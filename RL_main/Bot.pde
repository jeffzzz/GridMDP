class Bot {
  int ix, iy;   // location in maze
  int nstates, statex, statey;
  int last_action;
  float reward;
  float summed_reward;
  float alpha; // learning rate
  float gamma; // discount factor
  int Ne; //exploration threshold
  float Rp; //exploration reward
  float[][][] Q;
  int [][][] action_counts;
  float step_count;

  Bot() {
    nstates = maze.nx * maze.ny;   
    Q = new float[maze.ny][maze.nx][4]; // 4 actions
    action_counts = new int[maze.ny][maze.ny][4];
    alpha = 1.0;
    gamma = 0.99;
    Rp = 2.9;
    reset();
  }

  void reset() {
    home();
    resetQ();
  }

  void home() {
    // start in lower left corner
    //step_count = 1.0;
    alpha = 1.0;
    ix = 1;
    iy = maze.ny - 3;
    statex = ix;
    statey = iy; // convert position to state
    last_action = 4; // NONE
    reward = 0.0;
    summed_reward = 0.0;
    display();
  }

  void resetQ() {
    for (int y=0; y<maze.ny; y++) {
      for (int x=0; x<maze.nx; x++) {
        for (int a=0; a<4; a++) {
          action_counts[y][x][a] = 0;
          Q[y][x][a] = 0.0;
        }  
      }
    }
    /*for (int a=0; a<4; a++) {
      Q[0][1][a] = -1.0;
      Q[1][4][a] = -1.0;
      Q[2][5][a] = 3.0;
      Q[5][0][a] = 1.0;
      Q[5][1][a] = -1.0;
      Q[5][4][a] = -1.0;
      Q[5][5][a] = -1.0;
    }*/
  }


  void step() {
    int s0x,s0y, s1x, s1y, a0, a1;
    step_count += 1.0;
    if (reward == -1.0 || reward == 1.0 || reward == 3.0){  // reached the reward
      nextTrial();
    }
    else {
    s0x = statex;
    s0y = statey;
    a0 = pickAction();
    takeAction(a0); 
    s1x = statex;
    s1y = statey;
    a1 = pickAction();
    action_counts[s0y][s0x][a0]++;
    //alpha = 10000.0 / (9999.0 + 0.1*step_count);
    alpha = 6000.0 / (6000.0 + action_counts[s0y][s0x][a0]);
    Q[s0y][s0x][a0] = Q[s0y][s0x][a0] + alpha * (reward + gamma * Q[s1y][s1x][a1] - Q[s0y][s0x][a0]);
    }
  }

  int pickAction() {
    int action = int(random(4.0)); 
    float max = -999.0;
    float prob = random(1.0);
    float utility;
    float backup;
    int explore_count = 0;
    int [] explore = {0,0,0,0};
    for(int i = 0; i < 4; i++){
        if (action_counts[statey][statex][i] < Ne){
          utility = Rp;
          explore[explore_count] = i;
          explore_count++;
        }
        else
          utility = Q[statey][statex][i];
          
        backup = Q[statey][statex][i];
        
        if (explore_count > 0){
          float p = random(explore_count);
          action = explore[int(p)];
          float temp = random(1.0);
          if ((temp < 0.8) && (backup >= 3.0))
            action = i;
        }
        else {
          if (utility >= max){
            max = Q[statey][statex][i];
            action = i;
          }
        }
    }
    if (prob <= 0.8)
      return action;
    else if (prob <= 0.9)
      if (action == 0)
        return 3;
      else
        return action - 1;
    else
      if (action == 3)
        return 0;
      else
        return action + 1;
        
    
  }

  void display() {
    // yellow circle
    fill(250, 250, 0);
    float r = maze.w/2;
    ellipse(maze.xc[iy][ix], maze.yc[iy][ix], r, r);
  }

  void takeAction(int action) {
    last_action = action;
    int xold = ix;
    int yold = iy;
    if (action == NORTH) iy--;
    if (action == SOUTH) iy++;
    if (action == EAST) ix++;
    if (action == WEST) ix--; 
    if (maze.isWall(ix, iy)) {
      ix = xold;
      iy = yold;
    }
    reward = maze.val[iy][ix];
    summed_reward += reward;
    // if bot runs into wall, move bot back
    statex = ix;
    statey = iy;
  }
}

