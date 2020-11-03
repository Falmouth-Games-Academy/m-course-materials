package controllers.mctsdriver;

import java.awt.Graphics2D;
import java.util.List;

import framework.core.Game;

public interface RoutePlanner
{
	public void analyseMap(Game game, long dueTime);
	public boolean isFinishedPlanning();
	
	public List<Integer> getRoute();
	public int getNextWaypoint();
	public void advanceRoute();
	public double getEvaluation(Game game);
	
	public void draw(Graphics2D g);
}
