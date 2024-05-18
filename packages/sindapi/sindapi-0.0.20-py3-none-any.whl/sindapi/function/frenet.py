import numpy as np

from ..sindmap.utils.map_primitives import Polyline, Point

# 坐标系转化
# 找寻投影点
# point:二维数组，每行表示一个时间点的轨迹坐标（X，Y）
# refpoint:二维数组，每行表示一个离散点s的坐标（X，Y）
# 前者列数表示沿时间离散，后者列数表示沿距离离散
def RefPoint(point, refpoint):
    # 处理为3D坐标(T*L*2)以方便矩阵运算
    t = point.shape[0]
    l = refpoint.shape[0]
    point3d = np.repeat(point[:, np.newaxis, :], l, axis=1)
    refpoint3d = np.repeat(refpoint[np.newaxis, :, :], t, axis=0)
    # 计算欧式距离举矩阵，先做减法再求二范数，返回T行K列矩阵
    # 每个点表示轨迹点和参考点的欧式距离，第（t,l）个表示轨迹的第 t 个时间点与参考线的第 l 个点之间的欧氏距离
    vect = point3d - refpoint3d
    Euclid_Dis = np.linalg.norm(vect, axis=2)
    # 找出投影点:距离最近的点（axis等于1表示在行中查找最小值坐标）
    ProjIndex = np.argmin(Euclid_Dis, axis=1)
    ProjPoint = refpoint[ProjIndex]
    return [ProjIndex, ProjPoint]


# Cartesian转化为Frenet
def Carte2Fre(state, refpoint, dt=1.0):
    # 计算参考点
    # 取statematrix里面前两列（X,Y）
    # cartepoint = state.StateMatrix[:, :2]
    # 计算投影点
    [projindex, projpoint] = RefPoint(state, refpoint)
    # 测试：绘制两个曲线
    # UtilDrawing(cartepoint, refpoint, projpoint)

    # 计算S坐标：投影点到参考线上对应点的累积距离
    # 初始化S坐标的数组
    temp1 = np.array([0])
    temp2 = np.concatenate(
        (temp1, np.sqrt(np.sum(np.diff(refpoint, axis=0)**2, axis=1))), axis=0)
    S = np.cumsum(temp2)
    # projS = np.transpose(S[projindex, :])  # 修改
    projS = np.transpose(S[projindex])

    # 计算L坐标：轨迹点到投影点的距离
    projL = np.linalg.norm(state - projpoint, axis=1)
    # frenet_points = np.concatenate((projS, projL), axis=1)        修改
    frenet_points = np.concatenate((projS.reshape(-1, 1), projL.reshape(-1, 1)), axis=1)

    # 计算S相对于时间的一阶导数 ds/dt
    np.array([])
    # 将(ds_dt,dl_dt,d2s_dt2)补全:末尾增加一个和两个数
    ds_dt = np.diff(np.transpose(projS)) / dt
    ds = np.transpose(np.concatenate((ds_dt, np.array([ds_dt[-1]])), axis=0))
    # 计算L相对于时间的一阶导数 dl/dt
    dl_dt = np.diff(np.transpose(projL)) / dt
    dl = np.transpose(np.concatenate((dl_dt, np.array([dl_dt[-1]])), axis=0))
    # 计算S相对于时间的二阶导数 d^2S/dt^2
    d2s_dt2 = np.diff(ds_dt) / dt
    d2s = np.transpose(
        np.concatenate((d2s_dt2, np.array([d2s_dt2[-1]]), np.array([d2s_dt2[-1]])), axis=0))
    # 计算L相对于时间的二阶导数 d^2L/dt^2
    d2l_dt2 = np.diff(dl_dt) / dt
    d2l = np.transpose(
        np.concatenate((d2l_dt2, np.array([d2l_dt2[-1]]), np.array([d2l_dt2[-1]])), axis=0))
    # 组合
    FrenetPoint = np.concatenate((frenet_points, ds[:, np.newaxis], dl[:, np.newaxis], d2s[:, np.newaxis], d2l[:, np.newaxis]), axis=1)

    return FrenetPoint


