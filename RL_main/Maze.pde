class Maze {
  int nx, ny;       // number of cells in each direction
  int w;            // cell size (pixels)
  float[][] xc, yc; // cell coordinates (center)
  float[][] val = {
    {
      -0.04, -1.0, -0.04, -0.04, -0.04, -0.04
    }
    , 
    {
      -0.04, -0.04, -0.04, -10.0, -1.0, -0.04
    }
    , 
    {
      -0.04, -0.04, -0.04, -10.0, -0.04, 3.0
    }
    , 
    {
      -0.04, 0.0, -0.04, -10.0, -0.04, -0.04
    }
    , 
    {
      -0.04, -0.04, -0.04, -0.04, -0.04, -0.04
    }
    , 
    {
      1.0, -1.0, -0.04, -10.0, -1.0, -1.0
    }
  };      // cell value
  float WALL_VAL = -10.0;
  Maze() {
    nx = 6;
    ny = 6;
    w = 70;
    xc = new float[nx][ny];
    yc = new float[nx][ny];
    //val = new int[nx][ny];

    for (int i=0; i<ny; i++) {
      for (int j=0; j<nx; j++) {
        xc[i][j] = w*j + w/2;
        yc[i][j] = w*i + w/2;
      }
    }
  }

  boolean isWall(int ix, int iy) {
    if ( ix < 0 || ix > 5 || iy < 0 || iy > 5)
      return true;
    else if (val[iy][ix] == WALL_VAL)
      return true;
    else
      return false;
  }

  void showReward(float x, float y) {
    fill(255);
    textAlign(CENTER, CENTER);
    text("R", w*x + w/2, w*y + w/2);
  }

  void display() {
    fill(255);
    textAlign(CENTER, CENTER);
    stroke(50);
    for (int i=0; i<ny; i++) {
      for (int j=0; j<nx; j++) { 
        if (val[i][j] == WALL_VAL) {
          fill(100, 150, 250);
          rect(xc[i][j]-w/2, yc[i][j]-w/2, w, w);
        } else {
          fill(0);
          rect(xc[i][j]-w/2, yc[i][j]-w/2, w, w);
        }
        if (showV) {
          fill(255);
          textSize(12);
          text(val[i][j], xc[i][j], yc[i][j]);
        }    
        if (val[i][j] == -1.0 || val[i][j] == 1.0 || val[i][j] == 3.0) {
          showReward(j, i);
        }
        if (showQ) {
          int s = i + ny*j; // state
          if (val[i][j] != WALL_VAL) {
            fill(0, 255, 255);
            textAlign(CENTER, CENTER);
            textSize(9);
            // EAST
            pushMatrix();
            translate(xc[i][j]+30, yc[i][j]);
            rotate(HALF_PI);
            text(nf(bot.Q[i][j][EAST], 0, 3), 0, 0);
            popMatrix();
            // SOUTH
            pushMatrix();
            translate(xc[i][j], yc[i][j]+30);
            rotate(0);
            text(nf(bot.Q[i][j][SOUTH], 0, 3), 0, 0);
            popMatrix();
            //WEST
            pushMatrix();
            translate(xc[i][j]-30, yc[i][j]);
            rotate(-HALF_PI);
            text(nf(bot.Q[i][j][WEST], 0, 3), 0, 0);
            popMatrix();
            // NORTH
            pushMatrix();
            translate(xc[i][j], yc[i][j]-30);
            rotate(0);
            text(nf(bot.Q[i][j][NORTH], 0, 3), 0, 0);
            popMatrix();
          }
        }
      }
    }
  }
}

