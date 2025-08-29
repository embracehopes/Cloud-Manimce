# VS Code on Binder

[![PyPI](https://img.shields.io/pypi/v/jupyter-vscode-proxy)](https://pypi.org/project/jupyter-vscode-proxy/)
[![Install with conda](https://anaconda.org/conda-forge/jupyter-vscode-proxy/badges/version.svg)](https://github.com/conda-forge/jupyter-vscode-proxy-feedstock)

VS Code on Binder, because sometimes you need a real editor.  
已集成Manim动画库，可直接编写数学动画代码。

Try it: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/betatim/vscode-binder/master?urlpath=lab)

## 运行Manim示例
1. 启动Binder环境后，打开`examples/manim_demo.py`
2. 在终端执行：`manim -pql examples/manim_demo.py BasicAnimation`
3. 动画会自动生成并播放（`-pql`表示低质量快速预览）
