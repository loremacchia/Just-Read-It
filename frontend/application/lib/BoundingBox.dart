class BoundingBox {
  Map<String, double> rectangle;
  String text;
  
  BoundingBox(String text, double coord1, double coord2, double coord3, double coord4,){
    this.text = text;
    rectangle["x"] = coord1; //TODO capire se la posizione cambia
    rectangle["y"] = coord2;
    rectangle["width"] = coord3;
    rectangle["height"] = coord4;
  }

  double getRatio(){
    return rectangle["width"]/rectangle["height"];
  }

  double getArea(){
    return rectangle["width"]*rectangle["height"];
  }

  int getQuadrant(int w, int h) {
    double xPt = rectangle["x"] + rectangle["width"] / 2;
    double yPt = rectangle["y"] + rectangle["height"] / 2;
    int xQuad;
    int yQuad;
    if (xPt >= 0 && xPt < w / 3) {
      xQuad = 0;
    }
    else if (xPt >= w / 3 && xPt < w * 2 / 3) {
      xQuad = 1;
    }
    else {
      xQuad = 2;
    }
    if (yPt >= 0 && yPt < h / 3) {
      yQuad = 0;
    }
    else if (yPt >= h / 3 && yPt < h * 2 / 3) {
      yQuad = 1;
    }
    else {
      yQuad = 2;
    }
    return xQuad + yQuad * 3;
  }
}