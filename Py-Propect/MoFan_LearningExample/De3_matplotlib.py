import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
# x = np.linspace(-3, 3, 50)
# y1 = 2*x + 1
# y2 = x**2
# plt.figure()
# #set x limits
# plt.xlim((-1, 2))
# plt.ylim((-2, 3))
# # set new sticks
# new_sticks = np.linspace(-1, 2, 5)
# plt.xticks(new_sticks)
# # set tick labels
# plt.yticks([-2, -1.8, -1, 1.22, 3],#将y轴这五个数据分别对应以下五个单词
#            [r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$really\ good$'])
# # set line syles
# l1, = plt.plot(x, y1, label='linear line')#以下三句用于确定函数图像标签及其位置
# l2, = plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--', label='square line')
# plt.legend(handles=[l1,l2,], loc='upper right')
# print("new-sticks：", new_sticks)
# plt.show()
#在图片里添加注解------------------------------------------------------------------------------------------------------------
# x = np.linspace(-3, 3, 50)
# y = 2*x + 1
# plt.figure(num="figure", figsize=(8,5),)#num表示图片的名字
# plt.plot(x,y,linewidth=1)#此句用于画出函数图像，也可以是plt.scatter(x,y),画出散点图
# ax = plt.gca()#gca是get current axis的缩写，目的是获取当前的轴，返回的是坐标轴的对象
# #以下六句就把(0.0)点处于图片的中心，这里的spines
# ax.spines['right'].set_color("none")#将右边的轴设置为无色
# ax.spines['top'].set_color("none")#将上边的轴设置为无色
# ax.xaxis.set_ticks_position('bottom')#把x轴设置在bottom边
# ax.yaxis.set_ticks_position("left")#将y轴设置在left边
# ax.spines['bottom'].set_position(('data',0))#将x轴(这里就是bottom这个参数)设置在y轴的0位置
# ax.spines['left'].set_position(('data', 0))#将y轴设置在x轴的0位置
#
# x0 = 1
# y0 = 2*x0+1
# plt.scatter(x0,y0,s=50,color='b')#此句的目的是在图像中画出(x0,y0)点，s表示点的大小
# #下一个函数的目的是在图像中画出一条垂直于x轴的线段，并在图像中添加注解
# plt.annotate(r'$2x+1=%s$'%y0, xy=(x0,y0), xycoords='data', xytext=(+30,-30),
#              textcoords='offset points', fontsize=16,
#              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))#此句的目的是在图像中添加注解
# #下一句也是在图像中添加注解
# plt.text(-3.7, 3, r'$This\ is\ the\ some\ text.\ \mu\ \sigma_i\ \alpha_t$',
#             fontdict={'size':16, 'color':'r'})#此句的目的是在图像中添加注解`This is the some text. \mu \sigma_i \alpha_t`
#
# print(ax.get_xticklabels())#获取x轴的刻度标签
# plt.show()

#散点图p10------------------------------------------------------------------------------------------------------------
# n = 1024
# X = np.random.normal(0, 1, n)#生成了 n 个均值为 0，标准差为 1 的正态分布随机数
# Y = np.random.normal(0, 1, n)
# T = np.arctan2(Y, X)#此句效果是
# plt.scatter(X, Y, s=30, c=T, alpha=0.5)#s表示点的大小，c表示点的颜色，alpha表示透明度
# plt.xlim((-3, 3))
# plt.ylim((-3, 3))
# plt.xticks(())#此句效果是隐去x轴的刻度
# plt.yticks(())
# plt.show()
#柱状图p11------------------------------------------------------------------------------------------------------------
# n = 12
# X = np.arange(n)
# Y1 = (1 - X/float(n))*np.random.uniform(0.5, 1, n)#为一个新的 numpy 数组，其长度为 n，所有元素都在 0 到 0.5 之间，且元素的值有随机性。
# Y2 = (1 - X/float(n))*np.random.uniform(0.5, 1, n)
# plt.bar(X, Y1, facecolor='#9999ff', edgecolor='white')#facecolor表示柱状图的颜色，edgecolor表示柱状图的边缘颜色
# plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')
# #以下两个for循环是为了在柱状图上添加数值标签
# for x,y in zip(X, Y1):
#     plt.text(x, y+0.03, '%.2f'%y, ha='center', va='bottom')
# for x,y in zip(X, Y2):
#     plt.text(x, -y-0.03, '%.2f'%y, ha='center', va='top')
# plt.xlim(-.5, n)
# plt.ylim(-1.24,1.25)
# # plt.xticks(())
# # plt.yticks(())
# plt.show()
#等高线图p12------------------------------------------------------------------------------------------------------------
# def f(x, y):
#     return (1 - x/2 + x**5 + y**3)*np.exp(-x**2-y**2)
# n = 256
# x = np.linspace(-3, 3, n)
# y = np.linspace(-3, 3, n)
# X,Y = np.meshgrid(x, y)#meshgrid函数用于生成网格点坐标矩阵
# plt.contourf(X, Y, f(X, Y), 15, alpha=0.77, cmap=plt.cm.hot)#contourf函数是用来画等高线的，X,Y是坐标，f(X,Y)是高度，8表示等高线的密集程度，alpha表示透明度，cmap表示颜色
# C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidths=.5)#
# plt.clabel(C, inline=True, fontsize=10)
# plt.show()
#image图片p13------------------------------------------------------------------------------------------------------------
# a = np.array([0.313660827978, 0.365348418405, 0.423733120134,
#               0.365348418405, 0.439599930621, 0.525083754405,
#               0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)
# plt.imshow(a, interpolation='none', cmap='bone', origin='lower')#imshow函数是用来显示图片的，interpolation表示插值方法，cmap表示颜色，origin表示原点的位置
# plt.colorbar()
# plt.xticks(())
# plt.yticks(())
# plt.show()
#3D数据p14------------------------------------------------------------------------------------------------------------
# fig = plt.figure()
# ax = fig.add_axes(Axes3D(fig))#add_axes函数是添加一个三维坐标轴
# X = np.arange(-4, 4, 0.25)
# Y = np.arange(-4, 4, 0.25)
# X,Y = np.meshgrid(X, Y)#meshgrid函数用于生成网格点坐标矩阵
# R = np.sqrt(X**2 + Y**2)#
# Z = np.sin(R)
# ax.plot_surface( X, Y, Z, rstride=1, cstride= 1, cmap=plt.get_cmap('rainbow') )
# plt.show()
#subplot多合一显示p15------------------------------------------------------------------------------------------------------------
# plt.figure()
# plt.subplot(2,2,1)#表示将图片分成2行1列，此时的图片是第1个
# plt.plot([0,4], [0,2])#[0,1], [0,2]表示x轴的0到1，y轴的0到2
# plt.subplot(2,3,4)
# plt.plot([0,1], [0,2])
# plt.subplot(2,3,5)
# plt.plot([0,1], [0,2])
# plt.subplot(2,3,6)
# plt.plot([0,1], [0,2])
# plt.show()
#subplot分格显示p16------------------------------------------------------------------------------------------------------------

# 有三种方法分别为：subplot2grid, gridspec,
#P17图中图------------------------------------------------------------------------------------------------------------
# fig = plt.figure()
# x = [1,2,3,4,5,6,7]
# y = [1,3,4,2,5,8,6]
# left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
# ax1 = fig.add_axes([left, bottom, width, height])#此句就是在fig中添加一个坐标轴,这四个参数分别是左边界，下边界，宽度，高度在整个fig中的比例
# ax1.plot(x,y,'r')#画出x,y的图像
# ax1.set_xlabel('x')#设置x轴的标签
# ax1.set_ylabel('y')
# ax1.set_title('title')
# #以下是在上几句程序生成的大图中添加一个小图
# left, bottom, width, height = 0.2, 0.6, 0.2, 0.2
# ax1 = fig.add_axes([left, bottom, width, height])#此句就是在fig中添加一个坐标轴,这四个参数分别是左边界，下边界，宽度，高度在整个fig中的比例
# ax1.plot(y,x,'r')#画出x,y的图像
# ax1.set_xlabel('x')#设置x轴的标签
# ax1.set_ylabel('y')
# ax1.set_title('subplot1')
# plt.show()
#次坐标轴p18------------------------------------------------------------------------------------------------------------
# x = np.arange(0, 30, 0.0001)
# y1 = 2**np.sin(x)/np.sqrt(x+1)
# y2 = -1*y1
# fig, ax1 = plt.subplots()#返回一个图片对象(把它看成一个空白画布)和坐标轴(横坐标和纵坐标)，分别赋值给fig和ax1
# ax2 = ax1.twinx()#此句的目的是生成一个和ax1共享x轴的坐标轴
# ax1.plot(x, y1, 'g--')
# ax2.plot(x, y2, 'b-')
# ax1.set_xlabel('X data')
# ax1.set_ylabel('Y1', color='g')
# ax2.set_ylabel('Y2', color='b')
# plt.show()
#动画p19------------------------------------------------------------------------------------------------------------
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
fig, ax = plt.subplots()
x = np.arange(0,2*np.pi,0.01)
line, = ax.plot(x, np.sin(x))#在横纵坐标画出sinx的图像对象返回给line

def animate(i):#此函数的目的是在图像中画出sin(x+i/10)的图像，i表示第i帧
    line.set_ydata(np.sin(x+i/30))#set_ydata的意思是将y轴的数据设置为np.sin(x+i/10)
    return line,
def init():#此函数用于确定第一帧的内容
    line.set_ydata(np.sin(x))
    return line,
#以下是生成动画的函数
ani = animation.FuncAnimation(fig=fig, func=animate, frames=1000, init_func=init, interval=20, blit=True)
#以上几个参数：func表示动画函数，frames表示帧数，init_func作用确定第一帧的内容，interval表示更新频率，blit表示是否更新整个图像

plt.show()












































