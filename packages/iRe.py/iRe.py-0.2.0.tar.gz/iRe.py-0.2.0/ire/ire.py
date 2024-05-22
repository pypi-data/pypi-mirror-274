from dataclasses import dataclass
from inspect import getfullargspec
import os
from os import environ as env, getcwd, makedirs, rename
from os.path import islink, join
from tempfile import TemporaryDirectory
from typing import Literal, Optional, Union, TypeVar, Callable, Type

import pandas as pd
from IPython.display import display, HTML, Image
from utz import err

from ire.dvc import DvcConfig, is_dvc_repo, process_dvc_config
from ire.git import GitConfig, has_unpushed_commits, process_git_config
from ire.utils import md5_file, run


DEFAULT_ARTIFACTS_DIR = ".ire"
METADATA_KEY = 'iRe'

ParquetEngine = Literal['fastparquet', 'pyarrow', 'auto'] | None
Fmts = dict[str | Type, str]
ShowPlot = Union[None, 'png', 'html']
Fmt = Union[Literal['parquet'], Literal['plotly'], Literal['png']]


@dataclass
class Config:
    git: GitConfig
    dvc: DvcConfig
    dir: str = DEFAULT_ARTIFACTS_DIR
    relpath: str | None = None
    engine: ParquetEngine = None
    show: ShowPlot = None


# Default config values
config = Config(
    git='add',
    dvc='add' if is_dvc_repo() else False,
    dir=env.get('IRE_DIR', DEFAULT_ARTIFACTS_DIR),
    relpath=env.get('IRE_RELPATH'),
    engine=env.get('IRE_ENGINE'),
    show=env.get('IRE_SHOW'),
)


@dataclass
class Output:
    path: str
    md5: str


T = TypeVar("T")
DEFAULT_EXTENSION_OVERRIDES = {
    'plotly': 'json',
}


def chdir(path):
    os.chdir(path)
    config.dir = join(path, DEFAULT_ARTIFACTS_DIR)


def write_obj(
        obj: T,
        write: Callable,
        fmt: Fmt,
        name: str = None,
        dir: str = DEFAULT_ARTIFACTS_DIR,
        relpath: str = None,
        extension: str = None,
        git: GitConfig | None = None,
        dvc: DvcConfig | None = None,
        id: str | None = None,
        verbose: bool = False,
        engine: ParquetEngine = None,
        index: bool | None = None,
        fmts: Fmts | None = None,
):
    if extension is None:
        extension = DEFAULT_EXTENSION_OVERRIDES.get(fmt, fmt)

    def pre_write(path: str):
        if dvc and islink(path):
            # If the file is a symlink, we need to unprotect it before writing
            run('dvc', 'unprotect', path, verbose=verbose)

    write_kwargs = {}
    extra_metadata = {}
    spec = getfullargspec(write)
    if 'engine' in spec.args:
        if engine is None:
            engine = config.engine
        if engine:
            write_kwargs['engine'] = engine
    if 'index' in spec.args:
        write_kwargs['index'] = index
    if 'fmts' in spec.args:
        write_kwargs['fmts'] = fmts

    if name is None:
        with TemporaryDirectory(dir=getcwd()) as tmpdir:
            basename = f"tmp.{extension}"
            tmp_path = os.path.join(tmpdir, basename)
            write_rv = write(obj, tmp_path, **write_kwargs)
            md5 = md5_file(tmp_path)
            path = os.path.join(dir, f"{md5}.{extension}")
            makedirs(dir, exist_ok=True)
            pre_write(path)
            rename(tmp_path, path)
    else:
        path = os.path.join(dir, f"{name}.{extension}")
        makedirs(dir, exist_ok=True)
        pre_write(path)
        write_rv = write(obj, path, **write_kwargs)
    err(f"Saved {fmt} to {path}")
    path = process_dvc_config(dvc, path, verbose=verbose) or path
    md_path = join(relpath, path) if relpath else path
    process_git_config(git, path, verbose=verbose)
    if write_rv:
        extra_metadata.update(write_rv['metadata'])
    if id:
        extra_metadata['id'] = id
    metadata = { METADATA_KEY: { 'fmt': fmt, 'path': md_path, 'dvc': bool(dvc), **extra_metadata } }
    return metadata


def write_parquet(
        df: pd.DataFrame,
        path: str,
        engine: ParquetEngine = None,
        index: bool | None = None,
        fmts: Fmts | None = None,
):
    if engine is None:
        engine = 'auto'
    elif engine not in ('fastparquet', 'pyarrow'):
        raise ValueError(f"Unrecognized Parquet engine: {engine}")
    metadata = dict()
    index_names = list(filter(None, df.index.names))
    if index is not False:
        if index_names:
            metadata['index'] = index_names
    if fmts:
        cols = {}
        dtypes = {}
        for col, fmt in fmts.items():
            if isinstance(col, str):
                cols[col] = fmt
            elif col is int:
                dtypes['INT'] = fmt
            elif col is float:
                dtypes['FLOAT'] = fmt
            else:
                raise ValueError(f"Unrecognized column type: {col}")
        fmts_obj = {}
        if cols:
            fmts_obj['cols'] = cols
        if dtypes:
            fmts_obj['dtypes'] = dtypes
        metadata['fmts'] = fmts_obj
    df.to_parquet(path, engine=engine, index=bool(index_names) if index is None else index)
    return dict(metadata=metadata)


def write_image(img: Union[Image, bytes], path: str):
    with open(path, 'wb') as f:
        data = img.data if isinstance(img, Image) else img
        f.write(data)


def write_plotly(fig: 'Figure', path: str):
    fig_json = fig.to_json()
    with open(path, 'w') as f:
        f.write(fig_json)


def write_matplotlib(fig: 'plt.Figure', path: str):
    fig.savefig(path)


def maybe_handle_plotly(obj, kwargs, show: ShowPlot = None):
    try:
        from plotly.graph_objs import Figure
        if isinstance(obj, Figure):
            fig = obj
            metadata = write_obj(fig, write=write_plotly, fmt='plotly', **kwargs)
            if show == 'png':
                img_bytes = fig.to_image(format='png')
                display(Image(img_bytes), metadata=metadata)
            elif show == 'html':
                html = fig.to_html()
                display(HTML(html), metadata=metadata)
            else:
                display(fig, metadata=metadata)
            return True
    except ImportError:
        pass
    return False


def maybe_handle_matplotlib(obj, kwargs):
    try:
        import matplotlib.pyplot as plt
        if isinstance(obj, plt.Figure):
            fig = obj
            metadata = write_obj(fig, write=write_matplotlib, fmt='png', **kwargs)
            display(fig, metadata=metadata)
            plt.close()
            return True
    except ImportError:
        pass
    return False


def export(
        obj,
        name: str = None,
        dir: str = None,
        relpath: str = None,
        git: GitConfig | None = None,
        dvc: DvcConfig | None = None,
        id: str | None = None,
        verbose: bool = False,
        show: ShowPlot = None,
        engine: ParquetEngine = None,
        index: bool | None = None,
        fmts: Fmts | None = None,
):
    """Export a DataFrame, Image, or Plotly figure to disk, optionally committing to Git and/or DVC.

    Args:
        obj: The object to export. DataFrame ⟹ Parquet, Image ⟹ PNG, Plotly ⟹ JSON.
        name: basename of the file to write. If not provided, a name will be generated from the MD5 hash of the object.
        dir: directory in which to write the file. If not provided, the default directory will be used.
        relpath: relative path from output notebook location to `dir`, e.g. `..` if Papermill writes an output notebook
            into a subdirectory (relative to the input notebook path). In such a case, the iRe artifacts may be written
            to `.iRe/` under the parent directory, meaning the output notebook needs to prepend a `../` tp reach them.
        git: Git configuration. If `True`, the file will be added to the Git index. If `'commit'`, the file will be
            added to the index and committed. If `'commit!'`, the file will be added to the index and committed even if
            there are existing staged changes. If `None`, the default Git configuration will be used.
        dvc: DVC configuration. If `True`, the file will be added to the DVC cache. If `'commit'`, the file will be
            added to the cache and committed. If `'commit!'`, the file will be added to the cache and committed even if
            there are existing staged changes. If `None`, the default DVC configuration will be used.
        id: ID to embed in the output metadata, which iRe/www will turn into an HTML "id" attribute (useful for
            direct-linking to a cell in a rendered "report" view of a notebook).
        verbose: Whether to print verbose output.
        show: Whether to display the exported object. If `'png'`, a PNG image will be displayed; if `'html'`, an HTML
            representation will be displayed. If `None`, the object will not be displayed.
        engine: The Parquet engine to use when writing a DataFrame. If `None`, the default engine will be used.
        index: Whether to include the DataFrame index when writing to Parquet. If `None`, the index will be included if
            present.
        fmts: Column formatting info to include in the output metadata; string keys are column names, `Type`s are dtypes
            (e.g. `str`, `float` to set a fallback format for all columns of that type).
    """
    if git is None:
        git = config.git
    if dvc is None:
        dvc = config.dvc
    if dir is None:
        dir = config.dir
    if relpath is None:
        relpath = config.relpath
    if show is None:
        show = config.show
    if show:
        if show not in ['html', 'png']:
            raise ValueError(f"Unrecognized `show` param: {show}")

    kwargs = dict(dir=dir, relpath=relpath, name=name, git=git, dvc=dvc, id=id, verbose=verbose)
    if isinstance(obj, pd.DataFrame):
        df = obj
        kwargs.update(engine=engine, index=index, fmts=fmts)
        metadata = write_obj(obj=obj, write=write_parquet, fmt='parquet', **kwargs)
        html = df._repr_html_()
        return display(HTML(html), metadata=metadata)
    elif isinstance(obj, Image):
        metadata = write_obj(obj=obj, write=write_image, fmt='png', **kwargs)
        return display(obj, metadata=metadata)
    elif isinstance(obj, bytes):
        img = Image(obj)
        metadata = write_obj(obj=img, write=write_image, fmt='png', **kwargs)
        return display(img, metadata=metadata)
    elif not maybe_handle_plotly(obj, kwargs, show=show) and not maybe_handle_matplotlib(obj, kwargs):
        raise ValueError(f"Unrecognized export type: {type(obj)}")


def _ire_df_repr_html_(df):
    return export(df)


def push(
        git: bool = True,
        dvc: Optional[bool] = None,
        # Err on the side of letting the user know about Git/DVC pushes
        verbose: bool = True,
):
    if git:
        if has_unpushed_commits():
            run('git', 'push', verbose=verbose)
        else:
            if verbose:
                err("Git appears up to date, skipped push")
    if dvc or (dvc is None and config.dvc is not False):
        run('dvc', 'push', verbose=verbose)
