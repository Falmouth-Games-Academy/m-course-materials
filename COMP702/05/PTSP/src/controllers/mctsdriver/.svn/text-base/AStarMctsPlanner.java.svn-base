package controllers.mctsdriver;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import framework.core.*;
import framework.utils.*;
import controllers.mctsdriver.graph.*;


public class AStarMctsPlanner implements RoutePlanner
{
	/** The route planner will stop once the most exploited path has this many visits. */
	public int MCTS_ROUTEPLANNER_VISIT_LIMIT = 250;
	
	/** The radius of the first point on the A* path. */
	public double NAV_POINT_START_RADIUS = 250;
	
	/** The radius of the last point on the A* path. Radii of intermediate points are linearly interpolated. */
	public double NAV_POINT_END_RADIUS = 25;

	static public AStarMctsPlanner s_instance = null;
	
	private double m_uctExploration;
	
	/** Penalty for a 90 degree turn between entering and leaving a waypoint.
	 *  A 180 degree turn is worth twice this.
	 *  A 45 degree turn is worth 1-cos(45 degrees) = 0.292 times this. */
	public double WAYPOINT_TURN_PENALTY = 100;
	
	public AStarMctsPlanner(double uctExploration)
	{		
		if (s_instance == null)
			s_instance = this;

		m_uctExploration = uctExploration;
	}
	
	Graph m_graph = null;
	public Graph getGraph() { return m_graph; }
	
	Path[][] m_paths = null;
	Path getPath(Game game, int a, int b)
	{
		Path path = m_paths[a][b];
		
		if (path == null)
		{
			Vector2d pointFrom;
			Node nodeFrom;
			if (a == game.getWaypoints().size())
				pointFrom = game.getShip().s;
			else
				pointFrom = game.getWaypoints().get(a).s;
				
			nodeFrom = m_graph.getClosestNodeTo(pointFrom.x, pointFrom.y, false);
			Vector2d target = game.getWaypoints().get(b).s;
			Node nodeTo = m_graph.getClosestNodeTo(target.x, target.y, false);
			
			m_paths[a][b] = path = m_graph.getPath(nodeFrom.id(), nodeTo.id());
		}
		
		return path;
	}
	
	public void analyseMap(Game game, long dueTime)
	{
		if (m_root == null)
		{
			m_graph = new Graph(game);
			m_root = new TreeNode(null, new State(game), null);
			m_paths = new Path[game.getWaypoints().size() + 1][game.getWaypoints().size()];
		}
		
		long maxIteration = 0;
		while (System.currentTimeMillis() + maxIteration < dueTime)
		{
			long startTime = System.currentTimeMillis();
			runOneIteration(game);
			long timeTaken = System.currentTimeMillis() - startTime;
			if (timeTaken > maxIteration)
				maxIteration = timeTaken;
		}
	}

	Random m_rnd = new Random();
	
	public class Action
	{
		public Action(int waypointIndex) { m_waypointIndex = waypointIndex; }
		
		public int getWaypointIndex() { return m_waypointIndex; }
		
		private int m_waypointIndex;
		
		Path m_path = null;
		
		public Path getPath(State currentState)
		{
			if (m_path == null)
			{
				m_path = AStarMctsPlanner.this.getPath(currentState.m_game, currentState.m_waypointIndex, this.m_waypointIndex);
			}
			
			return m_path;
		}
	}
	
	class State
	{
		Game m_game;
		public Vector2d m_position;
		public Vector2d m_direction;
		public int m_waypointIndex;
		
		public boolean[] m_waypointsVisited;
		public double m_costSoFar;
		
		public State(Game game)
		{
			m_game = game.getCopy();
			m_position = m_game.getShip().s;
			m_direction = new Vector2d(0, -1);
			m_waypointIndex = m_game.getWaypoints().size();
			m_costSoFar = 0;
			
			m_waypointsVisited = new boolean[m_game.getWaypoints().size()];
			for (int i=0; i<m_game.getWaypoints().size(); i++)
			{
				m_waypointsVisited[i] = m_game.getWaypoints().get(i).isCollected();
			}
		}
		
		public List<Action> getActions()
		{
			List<Action> result = new ArrayList<Action>();
			
			for (int i=0; i<m_game.getWaypoints().size(); i++)
				if (!m_waypointsVisited[i])
					result.add(new Action(i));
			
			return result;
		}
		
		public void applyAction(Action action)
		{
			Path path = action.getPath(this);
			m_costSoFar += path.m_cost;
			
			Node firstNode = m_graph.getNode(path.m_points.get(0));
			Node secondNode = m_graph.getNode(path.m_points.get(1));
			Vector2d newDirection = new Vector2d(secondNode.x() - firstNode.x(), secondNode.y() - firstNode.y());
			newDirection.normalise();
			
			double cosAngle = newDirection.dot(m_direction);
			m_costSoFar += (1 - cosAngle) * WAYPOINT_TURN_PENALTY;
			
			m_waypointsVisited[action.m_waypointIndex] = true;
			m_position = m_game.getWaypoints().get(action.m_waypointIndex).s;
			m_direction = newDirection;
			m_waypointIndex = action.m_waypointIndex;
		}
		
		public boolean isTerminal()
		{
			for (boolean b : m_waypointsVisited)
				if (!b) return false;
					
			return true;
		}
	}
	
	class TreeNode
	{
		public TreeNode(TreeNode parent, State state, Action incomingAction)
		{
			m_parent = parent;
			if (m_parent != null)
				m_parent.m_children.add(this);
			
			m_incomingAction = incomingAction;
			
			m_unexpandedActions = state.getActions();
		}
		
		public double getAverageReward()
		{
			return m_totalReward / m_nVisits;
		}
		
		public void backpropagate(double simResult)
		{
			m_totalReward += simResult;
			m_nVisits ++;
		}
		
		private double m_totalReward = 0;
		public int m_nVisits = 0;
		
		public Action m_incomingAction = null;
		public TreeNode m_parent = null;
		public List<TreeNode> m_children = new ArrayList<TreeNode>();
		public List<Action> m_unexpandedActions = new ArrayList<Action>();
		
		public TreeNode getBestChild()
		{
			TreeNode bestChild = null;
			double bestChildScore = Double.NEGATIVE_INFINITY;
			
			for(TreeNode child : m_children)
			{
				double childScore;
				
				childScore = child.m_nVisits;
					
				//childScore += 1e-6 * m_rnd.nextDouble();
				
				if (childScore > bestChildScore)
				{
					bestChild = child;
					bestChildScore = childScore;
				}
			}
			
			return bestChild;
		}
	}
	
	TreeNode m_root = null;
	
	public int getRootVisits()
	{
		if (m_root == null)
			return 0;
		else
			return m_root.m_nVisits;
	}
	
	public int getRouteVisits()
	{
		if (m_root == null)
			return 0;
		
		TreeNode leaf = null;
		for (TreeNode node = m_root.getBestChild(); node != null; node = node.getBestChild())
			leaf = node;
		
		if (leaf == null || !leaf.m_unexpandedActions.isEmpty())
			return 0;
		else
			return leaf.m_nVisits;
	}
	
	public List<Action> getRouteActions()
	{
		List<Action> result = new ArrayList<Action>();
		
		for (TreeNode node = m_root.getBestChild(); node != null; node = node.getBestChild())
		{
			result.add(node.m_incomingAction);
		}
		
		return result;
	}
	
	public List<Integer> getRoute()
	{
		List<Integer> result = new ArrayList<Integer>();
		
		for (Action a : getRouteActions())
		{
			result.add(a.m_waypointIndex);
		}
		
		return result;
	}
	
	public void runOneIteration(Game game)
	{
		State state = new State(game);
		TreeNode node = m_root;
		
		// selection
		while (!state.isTerminal() && !node.m_children.isEmpty() && node.m_unexpandedActions.isEmpty())
		{
			TreeNode bestChild = null;
			double bestChildScore = Double.NEGATIVE_INFINITY;
			
			for(TreeNode child : node.m_children)
			{
				double childScore = child.getAverageReward()
						+ m_uctExploration * Math.sqrt(Math.log(node.m_nVisits) / (double)child.m_nVisits)
						+ 1e-6 * m_rnd.nextDouble();
				
				if (childScore > bestChildScore)
				{
					bestChild = child;
					bestChildScore = childScore;
				}
			}
			
			state.applyAction(bestChild.m_incomingAction);
			node = bestChild;
		}
		
		// expansion
		if (!node.m_unexpandedActions.isEmpty())
		{
			int actionIndex = m_rnd.nextInt(node.m_unexpandedActions.size());
			Action action = node.m_unexpandedActions.get(actionIndex);
			node.m_unexpandedActions.remove(actionIndex);
			state.applyAction(action);
			TreeNode newChild = new TreeNode(node, state, action);
			node = newChild;
		}
		
		// simulation
		while (!state.isTerminal())
		{
			List<Action> actions = state.getActions();
			if (actions.isEmpty()) break;
			state.applyAction(actions.get(m_rnd.nextInt(actions.size())));
		}
		
		// backpropagation
		double simulationResult = -state.m_costSoFar / 1000.0;

		for (int i=0; i<game.getWaypoints().size(); i++)
			if (state.m_waypointsVisited[i] == false)
				simulationResult -= 10;
		
		for (; node != null; node = node.m_parent)
		{
			node.backpropagate(simulationResult);
		}
	}
	
	BufferedImage m_graphImage = null;
	
	public void drawPath(Graphics2D g, Game game)
	{
		if (m_graphImage == null && m_graph != null)
		{
			m_graphImage = new BufferedImage(game.getMapSize().width, game.getMapSize().height, BufferedImage.TYPE_4BYTE_ABGR);
			Graphics2D gg = m_graphImage.createGraphics();
			m_graph.draw(gg);
			
			// Transparency
			for (int x=0; x<m_graphImage.getWidth(); x++)
				for (int y=0; y<m_graphImage.getHeight(); y++)
					m_graphImage.setRGB(x, y, m_graphImage.getRGB(x, y) + 0x70000000);
		}
		
		if (m_graphImage != null)
			g.drawImage(m_graphImage, 0, 0, null);
		
		if (m_root == null || m_root.m_children.isEmpty()) return;
		
		g.setColor(Color.pink);
		g.setFont(new Font("Arial", Font.BOLD, 10));
		
		int lastx = (int)game.getShip().s.x;
		int lasty = (int)game.getShip().s.y;
		
		for (TreeNode node = m_root.getBestChild(); node != null; node = node.getBestChild())
		{
			int nextx = (int)game.getWaypoints().get(node.m_incomingAction.m_waypointIndex).s.x;
			int nexty = (int)game.getWaypoints().get(node.m_incomingAction.m_waypointIndex).s.y;

			Path path = node.m_incomingAction.getPath(null);
			
			for(int i = 0; i < path.m_points.size()-1; ++i)
            {
                Node thisNode = m_graph.getNode(path.m_points.get(i));
                Node nextNode = m_graph.getNode(path.m_points.get(i+1));
                g.drawLine(thisNode.x(), thisNode.y(), nextNode.x(),nextNode.y());
                
                //g.drawOval(thisNode.x() - (int)MctsDriverController.NAV_POINT_RADIUS, thisNode.y() - (int)MctsDriverController.NAV_POINT_RADIUS,
                //		2*(int)MctsDriverController.NAV_POINT_RADIUS, 2*(int)MctsDriverController.NAV_POINT_RADIUS);
            }
			
			//g.drawLine(lastx, lasty, nextx, nexty);
			
			g.drawString(String.format("  %d", node.m_nVisits), nextx, nexty);
			
			lastx = nextx;
			lasty = nexty;
		}
	}

	@Override
	public int getNextWaypoint()
	{
		return m_root.getBestChild().m_incomingAction.m_waypointIndex;
	}

	@Override
	public void advanceRoute()
	{
		m_root = m_root.getBestChild();
		m_root.m_parent = null;
	}

	@Override
	public double getEvaluation(Game leafGameState)
	{
		List<AStarMctsPlanner.Action> route = getRouteActions();
		AStarMctsPlanner.Action currentAction = null;
		
		for (AStarMctsPlanner.Action a : route)
		{
			if (!leafGameState.getWaypoints().get(a.getWaypointIndex()).isCollected())
			{
				currentAction = a;
				break;
			}
		}
		
		if (currentAction == null)
			return 0;
		
		Path path = currentAction.getPath(null);
		int positionAlongPath = -1;
		for (int i=path.m_points.size()-1; i>=0; i--)
		{
			Node node = getGraph().getNode(path.m_points.get(i));
			double dx = node.x() - leafGameState.getShip().s.x;
			double dy = node.y() - leafGameState.getShip().s.y;
			
			double fractionAlongPath = (double)i / (double)path.m_points.size();
			double navPointRadius = NAV_POINT_START_RADIUS * (1 - fractionAlongPath) + NAV_POINT_END_RADIUS * fractionAlongPath;
			
			if (dx*dx + dy*dy <= navPointRadius*navPointRadius 
					&& leafGameState.getMap().checkObsFree((int)leafGameState.getShip().s.x, (int)leafGameState.getShip().s.y, node.x(), node.y()))
			{
				positionAlongPath = i;
				break;
			}
		}
		
		if (positionAlongPath != -1)
			return (double)positionAlongPath / (double)path.m_points.size();
		else
			return -1;
	}

	@Override
	public boolean isFinishedPlanning()
	{
		return getRouteVisits() >= MCTS_ROUTEPLANNER_VISIT_LIMIT;
	}

	@Override
	public void draw(Graphics2D g) {
		// TODO Auto-generated method stub
		
	}
}
