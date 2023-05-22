def det(x1,x2,x3):
    # fungsi determinan untuk menentukan posisi titik x3
    # relatif terhadap garis yang dibentuk x1 dan x2
    return (x1[0]*x2[1] + x3[0]*x1[1] + x2[0]*x3[1] 
            - x3[0]*x2[1] - x2[0]*x1[1] - x1[0]*x3[1])

def convex_hull(points):

    n = len(points)
    points.sort(key=lambda x: (x[0],x[1]))
    p1 = points[0]
    pn = points[n-1]

    # himpunan solusi hull
    global hull
    hull = [p1,pn]

    # membagi points menjadi dua bagian
    points_1 = list(filter(lambda x: (det(p1,pn,x) > 0), points))
    points_2 = list(filter(lambda x: (det(p1,pn,x) < 0), points))

    # rekursif untuk kedua bagian
    convex_hull_recursion(points_1,p1,pn,True)
    convex_hull_recursion(points_2,p1,pn,False)

    return hull

def convex_hull_recursion(points,p1,pn,isUpper):
    global hull

    if len(points) == 0: # tidak ada titik yang memenuhi
        return
    
    elif len(points) ==1: # hanya ada satu titik yang memenuhi
        p_idx = hull.index(p1 if isUpper else pn)
        hull.insert(p_idx+1,points[0])
        return
    else:
        p_idx = hull.index(p1 if isUpper else pn)
        points_det = [det(p1,pn,x) for x in points]

        # cari p extreme dan masukkan pada himpunan solusi
        idx_extreme = max(points_det) if isUpper else min(points_det)
        p_extreme = points[points_det.index(idx_extreme)]
        hull.insert(p_idx+1,p_extreme)

        # membagi lagi menjadi dua bagian
        if (isUpper):
            points_2 = list(filter(
                lambda x: (det(p_extreme,pn,x) > 0), points))
            points_1 = list(filter(
                lambda x: (det(p1,p_extreme,x) > 0), points))
        else:
            points_2 = list(filter(
                lambda x: (det(p_extreme,pn,x) < 0), points))
            points_1 = list(filter(
                lambda x: (det(p1,p_extreme,x) < 0), points))

        # rekursif untuk kedua bagian
        convex_hull_recursion(points_1,p1,p_extreme,isUpper)
        convex_hull_recursion(points_2,p_extreme,pn,isUpper)