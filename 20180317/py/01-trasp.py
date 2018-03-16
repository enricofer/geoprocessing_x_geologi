def trasp(t=0.5):
    layer = iface.activeLayer()
    if layer.opacity() == t:
        layer.setOpacity(1)  # double tra 0 e 1
    else:
        layer.setOpacity(t)
    iface.mapCanvas().refresh()