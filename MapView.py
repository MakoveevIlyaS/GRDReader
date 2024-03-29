from PyQt5 import QtCore, QtGui, QtWidgets

class MapView(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    pointColor = QtGui.QColor(255, 255, 255)
    isDragMode = False

    def __init__(self, parent):
        super(MapView, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo_h = QtWidgets.QGraphicsPixmapItem()
        #self.photos = [QtWidgets.QGraphicsPixmapItem()]
        self.photos = []
        self._scene.addItem(self._photo)  
        self._scene.addItem(self._photo_h) 
        #self._scene.addItem(self.photos[0])
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(130, 130, 130)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)  

    def hasPhoto(self):
        return not self._empty

    def fit(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())

        if not rect.isNull():
            self.setSceneRect(rect)

            if self.hasPhoto():
                u = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / u.width(), 1 / u.height())
                view = self.viewport().rect()
                scene = self.transform().mapRect(rect)
                factor = min(view.width() / scene.width(),
                             view.height() / scene.height())
                self.scale(factor, factor)

            self._zoom = 0

    def fit_h(self, scale=True):
        rect = QtCore.QRectF(self._photo_h.pixmap().rect())

        if not rect.isNull():
            self.setSceneRect(rect)

            if self.hasPhoto():
                u = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / u.width(), 1 / u.height())
                view = self.viewport().rect()
                scene = self.transform().mapRect(rect)
                factor = min(view.width() / scene.width(),
                             view.height() / scene.height())
                self.scale(factor, factor)

            self._zoom = 0

    def fit_new(self, scale=True):
       #rect = QtCore.QRectF(self._photo.pixmap().rect())
        rect = QtCore.QRectF(self.photos[len(self.photos)-1].pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)

            if self.hasPhoto():
                u = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / u.width(), 1 / u.height())
                view = self.viewport().rect()
                scene = self.transform().mapRect(rect)
                factor = min(view.width() / scene.width(),
                             view.height() / scene.height())
                self.scale(factor, factor)

            self._zoom = 0
            
    def setPhoto(self, pixmap=None):
        self._zoom = 0

        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.isDragMode = True
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.isDragMode = False
            self._photo.setPixmap(QtGui.QPixmap())

        self.fit()
      
    def setPhoto_h(self, pixmap=None):
        self._zoom = 0

        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.isDragMode = True
            self._photo_h.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.isDragMode = False
            self._photo_h.setPixmap(QtGui.QPixmap())

        self.fit_h()
    
    def setPhoto_new(self, pixmap=None):
        self._zoom = 0

        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.isDragMode = True
            #self._photo_h.setPixmap(pixmap)
            self.photos.append(QtWidgets.QGraphicsPixmapItem())
            self.photos[len(self.photos)-1].setPixmap(pixmap)
            self._scene.addItem(self.photos[len(self.photos)-1])
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.isDragMode = False
            #self._photo_h.setPixmap(QtGui.QPixmap())
            self.photos.append(QtWidgets.QGraphicsPixmapItem())
            self._scene.addItem(self.photos[len(self.photos-1)])
            self.photos[len(self.photos)-1].setPixmap(pixmap)

        self.fit_new()
    
    def Remove(self):
        #self._scene.removeItem(self.photos[len(self.photos)-1])
        #self.photos.pop()
        self.photos[1].setVisible(False)
        print("---", self._scene.items())
        print(len(self.photos))
        
    def Return(self):
        self.photos[1].setVisible(True)

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fit()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.isDragMode = False
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.isDragMode = True

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(MapView, self).mousePressEvent(event)

    def drawPoint(self, x, y):   
        return self._scene.addEllipse(QtCore.QRectF(x-1.5, y-1.5, 3, 3), QtGui.QPen(self.pointColor), QtGui.QBrush(self.pointColor))