from flask import current_app, redirect, jsonify
import jinja2

import os
from shutil import rmtree, move
import hashlib
import re
import uuid
import subprocess

TEX_SYMBOL_MAPPING = {
    '&': r'\&',
    '_': r'\_',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '\\': r'\textbackslash{}',
    '{': r'\{',
    '}': r'\}'
}

TEX_JINJA = None


def configure_jinja(app):
    global TEX_JINJA
    TEX_JINJA = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(app.config["TEX_WORKDIR"])
    )


def _to_camel_case(string):
    return re.sub("_(.)", lambda x: x.group(1).upper(), string)


def _prepare_recursive(arg):
    if isinstance(arg, dict):
        rv = {}
        for i in arg:
            rv[_to_camel_case(i)] = _prepare_recursive(arg[i])
        return rv

    if isinstance(arg, list):
        return list(map(_prepare_recursive, arg))

    if type(arg) == int:
        return arg

    if arg:
        arg = str(arg)
        return ''.join([ TEX_SYMBOL_MAPPING.get(c, c) for c in arg ])
    else:
        return ''


def _render(dict):
    template = TEX_JINJA.get_template('template.tex')
    return template.render(**dict)


def _download_picture(working_dir, pic_name):
    src = os.path.join(current_app.config["IMG_UPLOAD_PATH"], pic_name)
    dst = os.path.join(working_dir, pic_name)
    if not os.path.exists(dst):
        os.symlink(src, dst)


def render_protocol(protocol, raw=False):
    tmp_dir = os.path.join(current_app.config["TEX_WORKDIR"], uuid.uuid4().hex)
    os.mkdir(tmp_dir)

    # this replaces all the keys with camel case because they are a little
    # annoying in the .TeX template
    # Also it escapes all the LaTeX sequences
    protocol = _prepare_recursive(protocol)

    protocol['overview'] = r' \\ '.join(
        protocol['overview'].replace("\r\n", "\n").split("\n")
    )

    if protocol['facility']['picture']:
        _download_picture(tmp_dir, protocol['facility']['picture'])

    for entry in protocol['entries']:
        cat = entry['category']

        def mapper(standard):
            s = 'DIN {}{} {}'
            formatter = [ standard['din'], '', standard['description'] ]
            if standard.get('hasVersion', '') == 'Ja':
                formatter[1] = ':' + str(entry['categoryVersion'])
            return s.format(*formatter)

        cat['inspectionStandards'] = ', '.join(map(mapper,
                                                   cat['inspectionStandards']))
        for flaw in entry['flaws']:
            flaw['notes'] = flaw['notes']\
                .replace('\r\n', r'\newline ')\
                .replace('\n', r'\newline ')
            if flaw['picture']:
                _download_picture(tmp_dir, flaw['picture'])

    with open(os.path.join(tmp_dir, 'main.tex'), 'w') as dst_file:
        dst_file.write(_render(protocol))

    pargs = [
        'latexmk',
        '-interaction=nonstopmode',
        '-f',
        '-pdf',
        '-silent',
        'main.tex'
    ]
    compiler = subprocess.Popen(
        pargs,
        cwd=tmp_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    compiler.wait()
    """
    # twice because of lastpage ref (does not seem to be required for luatex)
    compiler = subprocess.Popen(pargs, cwd=tmp_dir)
    compiler.wait()
    """

    pdf = os.path.join(tmp_dir, 'main.pdf')
    with open(pdf, "rb") as f:
        h = hashlib.sha1()
        h.update(f.read())
        digest = h.hexdigest()

    if not os.path.exists(current_app.config["RENDER_SERVE_PATH"]):
        os.makedirs(current_app.config["RENDER_SERVE_PATH"])

    move(pdf, os.path.join(current_app.config["RENDER_SERVE_PATH"], digest + '.pdf'))
    rmtree(tmp_dir)

    if raw:
        return jsonify(file=digest)
    else:
        return redirect(f'/api/_display_render/{digest}')
