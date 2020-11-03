package controllers.mctsdriver;

import framework.utils.Vector2d;

public enum CompassDirection
{
	NORTH		( 0, -1),
	NORTHEAST	(+1, -1),
	EAST		(+1,  0),
	SOUTHEAST	(+1, +1),
	SOUTH		( 0, +1),
	SOUTHWEST	(-1, +1),
	WEST		(-1,  0),
	NORTHWEST	(-1, -1);
	
	private int m_dx, m_dy;
	private double m_cost;
	private Vector2d m_unitVector;
	
	CompassDirection(int dx, int dy)
	{
		m_dx = dx;
		m_dy = dy;
		m_cost = Math.sqrt(dx*dx + dy*dy);
		m_unitVector = new Vector2d(dx, dy);
		m_unitVector.normalise();
	}
	
	int dx() { return m_dx; }
	int dy() { return m_dy; }
	double cost() { return m_cost; }
	Vector2d unitVector() { return m_unitVector; }
	
	double positiveAngle(CompassDirection other)
	{
		double dot = unitVector().dot(other.unitVector());
		return Math.acos(dot);
	}
	
	public CompassDirection rotate(int steps)
	{
		 int i = (this.ordinal() + steps) % values().length;
		 if (i < 0) i += values().length;
		 return values()[i];
	}
}
