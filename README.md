# Girvan-Newman
## 介绍
本仓库中代码由[sikasjc的代码][1]修改而来，整合了代码运行逻辑，并使算法在数据量较大时能**输出中间成果**、显示进度。

关于**社区发现**和**Girvan-Newman算法**：

 - 社区发现：[Wiki][3]
 - sikasjc的博客：[GN算法][4]，[加权的GN算法][5]
 - Girvan–Newman算法：[Wiki][6]

## Python环境

 - Python 3.6.5
 - NetworkX 2.2
 - Matplotlib 2.2.2

## 数据集
使用[SNAP][6]提供的Twitter数据集（有向无权图）。

注：带权Girvan-Newman算法的测试代码中，边的权重为随机生成值。

[1]: https://github.com/sikasjc/CommunityDetection
[2]: https://en.wikipedia.org/wiki/Community_structure
[3]: https://sikasjc.coding.me/2017/12/20/GN/
[4]: https://sikasjc.github.io/2018/04/28/weighted_GN/
[5]: https://en.wikipedia.org/wiki/Girvan%E2%80%93Newman_algorithm
[6]: https://snap.stanford.edu/data/
