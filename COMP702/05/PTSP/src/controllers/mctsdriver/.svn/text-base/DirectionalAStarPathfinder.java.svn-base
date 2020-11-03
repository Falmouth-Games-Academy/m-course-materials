package controllers.mctsdriver;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import framework.core.Game;
import framework.core.Map;
import framework.utils.Vector2d;

public class DirectionalAStarPathfinder
{
	static final double ROTATION_PENALTY = 100;

	public class Node
	{
		public Node(int x, int y, CompassDirection d)
		{
			m_x = x; m_y = y; m_d = d;
		}
		
		private int m_x, m_y;
		private CompassDirection m_d;
		
		public int x() { return m_x; }
		public int y() { return m_y; }
		public CompassDirection d() { return m_d; }
		
		@Override
		public boolean equals(Object obj)
		{
			Node other = (Node)obj;
			return other != null 
				&& this.x() == other.x()
				&& this.y() == other.y()
				&& this.d() == other.d();
		}
		
		@Override
		public int hashCode()
		{
			return getHashCode(x(), y(), d());
		}
		
		private List<Edge> m_edges = null;
		
		public List<Edge> getEdges()
		{
			if (m_edges == null)
			{			
				m_edges = new ArrayList<Edge>();
				
				for (CompassDirection d2 : CompassDirection.values())
				{				
					int x2 = x() + d2.dx() * m_granularity;
					int y2 = y() + d2.dy() * m_granularity;
					
					if (x2 >= 0 && y2 >= 0 && x2 < m_map.getMapWidth() && y2 < m_map.getMapHeight() && m_map.checkObsFree(x(), y(), x2, y2))
					{
						Node neighbour = getNode(x2, y2, d2);
						m_edges.add(new Edge(this, neighbour));
					}
				}
			}
			
			return m_edges;
		}
		
		Edge cameFrom = null;
		double g, h;
	
	}
	
	public class Edge
	{
		private Node m_from, m_to;
		private double m_cost;
		
		public Edge(Node from, Node to)
		{
			m_from = from;
			m_to = to;
			
			m_cost = calcCost();
		}
		
		private double calcCost()
		{
			int dx = m_to.x() - m_from.x();
			int dy = m_to.y() - m_from.y();
			int dd = 0;
			
			if (m_from.d() != m_to.d())
				dd = (int)Math.round(m_from.d().positiveAngle(m_to.d()) / (Math.PI * 0.25));
			
			return Math.sqrt(dx*dx + dy*dy) + dd*ROTATION_PENALTY;
		}
		
		public Node from() { return m_from; }
		public Node to() { return m_to; }
		public double cost() { return m_cost; }
	}
		
	
	int getHashCode(int x, int y, CompassDirection d)
	{
		return x * 100000000 + y * 10000 + d.ordinal();
	}
	
	Map m_map;
	int m_granularity;
	
	public DirectionalAStarPathfinder(Game game, int granularity)
	{
		m_map = game.getMap();
		m_granularity = granularity;
	}
	
	HashMap<Integer, Node> m_nodes = new HashMap<Integer, Node>();
	
	Node getNode(int x, int y, CompassDirection d)
	{
		int key = getHashCode(x, y, d);
		Node node = m_nodes.get(key);
		if (node == null)
		{
			node = new Node(x, y, d);
			m_nodes.put(key, node);
		}
		return node;
	}
	
	public Node getClosestNodeTo(double x, double y, CompassDirection d)
	{
		return getNode(
				(int)(Math.round(x / m_granularity) * m_granularity),
				(int)(Math.round(y / m_granularity) * m_granularity),
				d);
	}

	private HashMap<Node, HashMap<Node, List<Edge>>> m_cachedPaths = new HashMap<Node, HashMap<Node,List<Edge>>>();
	
	public List<Edge> getPath(Node start, Vector2d goal)
	{
		Node goalNode = getClosestNodeTo(goal.x, goal.y, start.d());
		
		HashMap<Node, List<Edge>> map = m_cachedPaths.get(start);
		if (map != null)
		{
			List<Edge> path = map.get(goalNode);
			if (path != null)
				return path;
		}
		
		List<Edge> path = computePath(start, goalNode.x(), goalNode.y());
		
		if (map == null)
		{
			map = new HashMap<Node, List<Edge>>();
			m_cachedPaths.put(start, map);
		}
		
		map.put(goalNode, path);
		
		return path;
	}
	
	private List<Edge> computePath(Node start, int goalX, int goalY)
	{
		Set<Node> closedSet = new HashSet<Node>();
		Set<Node> openSet = new HashSet<Node>(); openSet.add(start);

		start.cameFrom = null;
		start.g = 0;
		start.h = getHeuristicEstimate(start, goalX, goalY);
		
		while (!openSet.isEmpty())
		{
			// Get node with lowest f score
			Node current = null;
			double currentFScore = Double.POSITIVE_INFINITY;
			
			for (Node n : openSet)
			{
				if (n.g + n.h < currentFScore)
				{
					current = n;
					currentFScore = n.g + n.h;
				}
			}
			
			if (current.x() == goalX && current.y() == goalY)
			{
				LinkedList<Edge> result = new LinkedList<Edge>();
				for (Edge edge = current.cameFrom; edge != null; edge = edge.from().cameFrom)
					result.addFirst(edge);
				
				return result;
			}
			
			openSet.remove(current);
			closedSet.add(current);
			
			for (Edge edge : current.getEdges())
			{
				Node neighbour = edge.to();
				
				if (closedSet.contains(neighbour)) continue;
				
				double tentativeG = current.g + edge.cost();
				boolean tentativeIsBetter = false;
				
				if (!openSet.contains(neighbour))
				{
					openSet.add(neighbour);
					neighbour.h = getHeuristicEstimate(neighbour, goalX, goalY);
					tentativeIsBetter = true;
				}
				else
				{
					tentativeIsBetter = (tentativeG < neighbour.g);
				}
				
				if (tentativeIsBetter)
				{
					neighbour.cameFrom = edge;
					neighbour.g = tentativeG;
				}
			}
		}
		
		return null;
	}
	
	protected double getHeuristicEstimate(Node node, int goalX, int goalY)
	{
		int dx = goalX - node.x();
		int dy = goalY - node.y();
		
		Vector2d directionToGoal = new Vector2d(dx, dy);
		directionToGoal.normalise();
		Vector2d directionOfTravel = new Vector2d(node.d().dx(), node.d().dy());
		directionOfTravel.normalise();
		
		double dd = 0;
		if (dx != 0 || dy != 0)
			dd = ROTATION_PENALTY*4 * 0.5 * (1 - directionToGoal.dot(directionOfTravel));
		
		return Math.sqrt(dx*dx + dy*dy) + dd;
	}
	
	public double getPathLength(List<Edge> path)
	{
		double length = 0;
		for (Edge e : path)
			length += e.cost();
		return length;
	}
	
}
