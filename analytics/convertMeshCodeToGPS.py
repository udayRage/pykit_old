from jpmesh import parse_mesh_code
def lat_lon_meshcodes(in_file,out_file):
    lines=[]
    val=[]
    with open(in_file, 'r') as k:
        for line in k:
            lines.append(line)
            li = line.split()
            val.append(li)
    kq=1
    with open(out_file, 'w') as f:
        for i in range(len(lines)):
            for m in val[i]:
                mesh = parse_mesh_code(m)
                mesh_center = mesh.south_west + (mesh.size / 2.0)
                x = (mesh_center.lon.degree, mesh_center.lat.degree)
                n_w = str((str(mesh.south_west.lon.degree) + ' ' + str(mesh.south_west.lat.degree),
                           str(mesh.south_west.lon.degree) + ' ' + str(
                               mesh.south_west.lat.degree + mesh.size.lat.degree),
                           str(mesh.south_west.lon.degree + mesh.size.lon.degree) + ' ' + str(
                               mesh.south_west.lat.degree + mesh.size.lat.degree),
                           str(mesh.south_west.lon.degree + mesh.size.lon.degree) + ' ' + str(
                               mesh.south_west.lat.degree),
                           str(mesh.south_west.lon.degree) + ' ' + str(mesh.south_west.lat.degree)))
                # n_w.replace("'", "")
                n_w = 'POLYGON(' + n_w + ')'
                u_s=str(n_w)
                u_s.replace("'", "")
                print(u_s)
                f.write('%s' % m.rstrip())
                f.write('\t%s' % kq)
                f.write('\t%s' % u_s)
                #             f.write(' %s'%str(x))
                f.write('\n')
            kq += 1
        f.close()
    lin=[]
    line_s=[]
    with open(out_file, 'r') as r:
        for line in r:
            pattern = line.replace("'", "")
            line_s.append(pattern)
    r.close()
    with open(out_file, 'w') as f:
        for x in line_s:
            f.write('%s' % str(x))
    f.close()

import sys
lat_lon_meshcodes(sys.argv[1],sys.argv[2])
