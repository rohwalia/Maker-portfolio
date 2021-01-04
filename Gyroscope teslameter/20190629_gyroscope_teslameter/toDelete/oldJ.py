
xJArray = np.linspace(-params.nR, params.nR, nXJ)
yJArray = np.linspace(-params.nR, params.nR, nXJ)
xJMg, yJMg = np.meshgrid(xJArray, yJArray)

jxMat, jyMat, jMat = [], [], []
dX = xArray[1]-xArray[0]
dY = yArray[1]-yArray[0]
for y in yJArray:
    jxMat.append([])
    jyMat.append([])
    jMat.append([])
    for x in xJArray:
        jx= 0
        jy = 0

        r = math.sqrt(x ** 2 + y ** 2)
        phi = math.atan2(y, x) % (2 * math.pi)

        # correct by the magnetic force and be careful to displace points just outside the magnetic field to be
        # slightly inside the magnetic field
        """
        if r >= params.r0-params.dR/2 and r <= params.r1+params.dR/2 and phi <= params.phi1:
            r=max(r,params.r0+params.dR/2)
            r=min(r,params.r1-params.dR/2)
            x= r*math.cos(phi)
            y=r*math.sin(phi)
            jx += 2 * params.B * params.omega * r * math.cos(phi) * dX
            jy += 2 * params.B * params.omega * r * math.sin(phi) * dY
        """
        if r >= params.r0 and r <= params.r1 and phi <= params.phi1:
            jx += 2 * params.B * params.omega * r * math.cos(phi) * dX
            jy += 2 * params.B * params.omega * r * math.sin(phi) * dY

        sp0 = uF(x,y)-uF(x-dX,y)
        if not math.isnan(sp0):
            jx+= sp0
        sp1 = uF(x+dX,y)-uF(x,y)
        if not math.isnan(sp1):
            jx+=sp1


        sp0 = uF(x, y) - uF(x, y-dY)
        if not math.isnan(sp0):
            jy += sp0
        sp1 = uF(x, y+dY) - uF(x, y)
        if not math.isnan(sp1):
            jy += sp1

        jx/=(dX*params.sigma)
        jy/=(dY*params.sigma)

        j = math.sqrt(jx**2+jy**2)
        if j!=0:
            jx/=j
            jy/=j

        jxMat[-1].append(jx)
        jyMat[-1].append(jy)
        jMat[-1].append(j)

jxMat = np.array(jxMat)
jyMat = np.array(jyMat)
jMat = np.array(jMat)
