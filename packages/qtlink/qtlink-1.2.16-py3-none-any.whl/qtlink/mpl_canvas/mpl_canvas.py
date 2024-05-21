from PySide6.QtWidgets import QWidget


class MplCanvas(QWidget):
    """在qt中使用matplotlib绘制图像"""

    def __init__(self, width: float = 5, height: float = 4, dpi: int = 100, enable_toolbar: bool = True, parent=None):
        """
        :param width: 图像宽度
        :param height: 图像高度
        :param dpi: 图像dpi
        :param enable_toolbar: 是否启用顶部工具栏
        :param parent: 所属的ui父类
        """
        from matplotlib import pyplot as plt
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
            NavigationToolbar2QT as NavigationToolbar
        from matplotlib.figure import Figure
        from PySide6.QtWidgets import QVBoxLayout
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        super(MplCanvas, self).__init__(parent)
        self.canvas = FigureCanvas(Figure(figsize=(width, height), dpi=dpi, constrained_layout=True))
        self.ax = self.canvas.figure.subplots()

        self.vertical_layout = QVBoxLayout()
        if enable_toolbar:
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.canvas)
        self.setLayout(self.vertical_layout)

    def clear_canvas(self):
        """清空画布"""
        self.canvas.figure.clear()
        self.ax = self.canvas.figure.subplots()
        self.canvas.draw_idle()

    def plot_lines(self, data: list[dict],
                   x_label: str = '',
                   y_label: str = '',
                   title: str = '',
                   marker='o',
                   markersize=3,
                   *args, **kwargs):
        """绘制点线图
        :param data: 每个点的数据使用字典存储，结构为{'x': , 'y': , 'label': }
        :param x_label: x轴名称
        :param y_label: y轴名称
        :param title: 图像名称
        :param marker: 数据点样式
        :param markersize: 数据点大小
        :param args: ax.plot函数接收的其他参数
        :param kwargs: ax.plot函数接收的其他参数
        """
        enable_legend = False
        for item in data:
            if item.get('label'):
                enable_legend = True
                self.ax.plot(item['x'], item['y'], label=item['label'], marker=marker, markersize=markersize, *args, **kwargs)
            else:
                self.ax.plot(item['x'], item['y'], marker=marker, markersize=markersize, *args, **kwargs)

        # 设置轴标签和标题
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        if enable_legend:
            self.ax.legend(loc="upper left", framealpha=0.6)
        self.canvas.draw_idle()

    def plot_bars(self,
                  data: list[dict],
                  x_label: str = '',
                  y_label: str = '',
                  title: str = "",
                  width: float = 0.5,
                  alpha=0.9,
                  *args, **kwargs):
        """绘制多组对比直方图
        :param data: 每个点的数据使用字典存储，结构为{'x': , 'y': , 'label': }
        :param x_label: x轴名称
        :param y_label: y轴名称
        :param title: 图像名称
        :param width: 直方图宽度
        :param alpha: 直方图透明度
        :param args: ax.bar函数接收的其他参数
        :param kwargs: ax.bar函数接收的其他参数
        """
        n = len(data)
        enable_legend = False
        for i, item in enumerate(data):
            if item.get('label'):
                enable_legend = True
            offset = width / 2 * (n - 2 * i - 1)
            x_list = [x - offset for x in item['x']]
            y_list = item['y']
            self.ax.bar(x_list, y_list, width=width, label=item['label'], alpha=alpha, *args, **kwargs)

        # 设置轴标签和标题
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        if enable_legend:
            self.ax.legend(loc="upper left", framealpha=0.6)
        self.canvas.draw_idle()
