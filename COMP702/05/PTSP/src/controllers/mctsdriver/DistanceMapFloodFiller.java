package controllers.mctsdriver;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.Queue;

import javax.imageio.ImageIO;

//import wpm.mjpeg.MJPEGGenerator;

import framework.core.Map;
import framework.core.Ship;
import framework.utils.Vector2d;

public class DistanceMapFloodFiller
{
	double[][] m_distanceMap;
	int m_width, m_height;
	
	static final double c_wall = Double.NEGATIVE_INFINITY;
	static final double c_empty = Double.POSITIVE_INFINITY;
	
	private void init(Map map, int originX, int originY)
	{
		m_width = map.getMapWidth();
		m_height = map.getMapHeight();
		
		
		m_distanceMap = new double[m_width][m_height];
		
		
		for (int x=0; x<m_width; x++)
			for (int y=0; y<m_height; y++)
				if (map.isObstacle(x, y))
					m_distanceMap[x][y] = c_wall;
				else
					m_distanceMap[x][y]= c_empty;
		
		makeWallsFatter(map);

		floodFill(originX, originY);
	}
	
	public DistanceMapFloodFiller(Map map, int originX, int originY)
	{
		init(map, originX, originY);
	}
	
	public DistanceMapFloodFiller(Map map, Vector2d origin)
	{
		init(map, (int)origin.x, (int)origin.y);
	}
	
	void makeWallsFatter(Map map)
	{
		/*
		int r = Ship.SHIP_RADIUS;
		double r2 = (r - 0.2) * (r - 0.2);
		
		for (int x=0; x<m_width; x++)
		{
			for (int y=0; y<m_height; y++)
			{
				if (m_distanceMap[x][y] == c_wall) continue;
				
				for (int dx=-r; dx<=r; dx++) for (int dy=-r; dy<=r; dy++)
				{
					if (dx!=0 && dy!=0) continue;
					
					if ((map.isOutsideBounds(x+dx, y+dy) || map.isObstacle(x+dx, y+dy)) && dx*dx + dy*dy <= r2)
					{
						m_distanceMap[x][y] = c_wall;
						break;
					}
				}
			}
		}*/
		
		int wallsToAdd1 = 0;
		int wallsToAdd2 = 0; 
		
		for (int x=0; x<m_width; x++)
		{
			for (int y=0; y<m_height; y++)
			{
				if (wallsToAdd1 > 0)
				{
					m_distanceMap[x][y] = c_wall;
					wallsToAdd1--;
				}
				
				if (wallsToAdd2 > 0)
				{
					m_distanceMap[x][m_height-y-1] = c_wall;
					wallsToAdd2--;
				}
				
				if (map.isObstacle(x,y))
				{
					wallsToAdd1 = 3;
				}
				if (map.isObstacle(x,m_height-y-1))
				{
					wallsToAdd2 = 3;
				}
			}
		}
		wallsToAdd1 = 0;
		wallsToAdd2 = 0; 
		
		for (int y=0; y<m_height; y++)
		{
			for (int x=0; x<m_width; x++)
			{
				if (wallsToAdd1 > 0)
				{
					m_distanceMap[x][y] = c_wall;
					wallsToAdd1--;
				}
				
				if (wallsToAdd2 > 0)
				{
					m_distanceMap[m_width-x-1][y] = c_wall;
					wallsToAdd2--;
				}
				
				if (map.isObstacle(x,y))
				{
					wallsToAdd1 = 3;
				}
				if (map.isObstacle(m_width-x-1,y))
				{
					wallsToAdd2 = 3;
				}
			}
		}
	}
	
	public double getDistance(int x, int y)
	{
		if (x>=0 && y>=0 && x<m_width && y<m_height)
			return m_distanceMap[x][y];
		else
			return c_wall;
	}
	
	public double getDistance(Vector2d p)
	{
		return getDistance((int)p.x, (int)p.y);
	}
	
	double getGradientInDirection(int x, int y, int dx, int dy)
	{
		double a = m_distanceMap[x-dx][y-dy];
		double b = m_distanceMap[x][y];
		double c = m_distanceMap[x+dx][y+dy];
		
		if (a == c_wall && c == c_wall)
			return 0;
		else if (a == c_wall)
			return c - b;
		else if (c == c_wall)
			return b - a;
		else
			return (c - a) * 0.5;
	}
	
	public Vector2d getGradient(int x, int y)
	{
		return new Vector2d(getGradientInDirection(x, y, 1, 0), getGradientInDirection(x, y, 0, 1));
	}
	
	public Vector2d getGradient(Vector2d p)
	{
		return getGradient((int)p.x, (int)p.y);
	}
	
	class QueueItem
	{
		public int x,y;
		private  double d;
		public QueueItem(int xx, int yy, double dd) { x=xx; y=yy; d=dd; }
	}
	
	Queue<QueueItem> q;
	
	// Leave this as 1 for now -- values > 1 will cause it to miss 1-pixel obstacles! 
	static final int RADIUS = 1;
	
	static double[][] s_radiusDistances = null;
	
	double getMinDist(int x, int y)
	{
		if (s_radiusDistances == null)
		{
			s_radiusDistances = new double[RADIUS*2+1][RADIUS*2+1];
			
			for (int rx=-RADIUS; rx<=RADIUS; rx++) for (int ry=-RADIUS; ry<=RADIUS; ry++)
			{
				s_radiusDistances[rx+RADIUS][ry+RADIUS] = Math.sqrt(rx*rx + ry*ry);
			}
		}
		
		double result = m_distanceMap[x][y];
		
		for (int rx=-RADIUS; rx<=RADIUS; rx++) for (int ry=-RADIUS; ry<=RADIUS; ry++)
		{
			if (rx==0 && ry==0) continue;
			if (x+rx < 0 || x+rx >= m_width || y+ry < 0 || y+ry >= m_height) continue;
			
			double d = m_distanceMap[x+rx][y+ry];
			if (d == c_wall) continue;

			d += s_radiusDistances[rx+RADIUS][ry+RADIUS];
			
			if (d < result) result = d;
		}
		
		return result;
	}
	
	void scan(int x, int y, int dx, boolean queuedAbove, boolean queuedBelow)
	{
		if (x < 0 || x >= m_width) return;
		
		x += dx;
		double d = getMinDist(x, y);
		
		int step = 0;
		while (x >= 0 && x < m_width && m_distanceMap[x][y] > d)
		{
			m_distanceMap[x][y] = d;
			
			if (y > 0)
			{
				if (m_distanceMap[x][y-1] > d+1)
				{
					if (!queuedAbove)
					{
						q.add(new QueueItem(x, y-1, d+1));
						queuedAbove = true;
					}
				}
				else
					queuedAbove = false;
			}
			
			if (y < m_height-1)
			{
				if (m_distanceMap[x][y+1] > d+1)
				{
					if (!queuedBelow)
					{
						q.add(new QueueItem(x, y+1, d+1));
						queuedBelow = true;
					}
				}
				else
					queuedBelow = false;
			}
	
			x += dx;
			step++;
			
			d = getMinDist(x, y);
		}
	}
	
	//static final boolean WRITE_DEBUG_MOVIE = true;
	static final boolean WRITE_DEBUG_MOVIE = false;
	static final int DEBUG_MOVIE_FRAME_LIMIT = 10000;
	
	void floodFill(int x, int y)
	{
		q = new LinkedList<QueueItem>();
		q.add(new QueueItem(x, y, 0));
		
		int step = 0;
		
		/*MJPEGGenerator debugMovie = null;
		if (WRITE_DEBUG_MOVIE)
			try {
				debugMovie = new MJPEGGenerator(new File("floodFill_debug.avi"), m_width, m_height, 10, DEBUG_MOVIE_FRAME_LIMIT);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}*/
		
		for (QueueItem n = q.poll(); n != null; n = q.poll())
		{
			//dump(String.format("C:\\epowley_local\\temp\\flood\\step%d.png", step++));
			
			if (m_distanceMap[n.x][n.y] > n.d)
			{
				/*if (debugMovie != null)
				{
					System.out.print("Writing frame "); System.out.println(step);
					
					try {
						BufferedImage bi = dumpImage();
						bi.setRGB(n.x, n.y, 0xFFFFFF);
						debugMovie.addImage(bi);
					} catch (Exception e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}

					step++;
					if (step > DEBUG_MOVIE_FRAME_LIMIT)
					{
						System.out.println("Finished debug movie");
						
						try {
							debugMovie.finishAVI();
						} catch (Exception e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						debugMovie = null;
					}
				}*/
				
				m_distanceMap[n.x][n.y] = n.d;
				
				boolean queuedAbove = (n.y > 0 && m_distanceMap[n.x][n.y-1] > n.d+1);
				if (queuedAbove)
					q.add(new QueueItem(n.x, n.y-1, n.d+1));
					
				boolean queuedBelow = (n.y < m_height-1 && m_distanceMap[n.x][n.y+1] > n.d+1);
				if (queuedBelow)
					q.add(new QueueItem(n.x, n.y+1, n.d+1));
				
				scan(n.x, n.y, -1, queuedAbove, queuedBelow);
				scan(n.x, n.y, +1, queuedAbove, queuedBelow);
			}
		}
		
		/*if (debugMovie != null)
		{
			System.out.println("Finished debug movie");
			
			try {
				debugMovie.finishAVI();
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			debugMovie = null;
		}*/
	}
	
	BufferedImage dumpImage()
	{
		BufferedImage bi = new BufferedImage(m_width, m_height, BufferedImage.TYPE_INT_RGB);
		
		for (int y=0; y<m_height; y++)
		{
			for (int x=0; x<m_width; x++)
			{
				Color color;
				if (m_distanceMap[x][y] == c_wall)
					color = Color.gray;
				else if (m_distanceMap[x][y] == c_empty)
					color = Color.black;
				else
					color = new Color(Color.HSBtoRGB((float)m_distanceMap[x][y] / 200.0f, 1.0f, 0.5f));
				
				bi.setRGB(x, y, color.getRGB());
				
			}
		}
		
		for (QueueItem n : q)
		{
			bi.setRGB(n.x, n.y, Color.white.getRGB());
		}
		
		return bi;
	}
	
	BufferedImage dumpGradientImage()
	{
		BufferedImage bi = new BufferedImage(m_width, m_height, BufferedImage.TYPE_INT_RGB);
		
		for (int y=0; y<m_height; y++)
		{
			for (int x=0; x<m_width; x++)
			{
				Color color;
				if (m_distanceMap[x][y] == c_wall)
					color = Color.gray;
				else
				{
					Vector2d grad = getGradient(x, y);
					float r = (float)grad.x * 0.5f + 0.5f;
					if (r < 0.0f) r = 0.0f; if (r > 1.0f) r = 1.0f;
					float g = (float)grad.y * 0.5f + 0.5f;
					if (g < 0.0f) g = 0.0f; if (g > 1.0f) g = 1.0f;
					color = new Color(r,g,0);
				}
				
				bi.setRGB(x, y, color.getRGB());
				
			}
		}
		
		return bi;
	}
	
	void dump(String filename)
	{
		try
		{
			ImageIO.write(dumpImage(), "png", new File(filename));
			ImageIO.write(dumpGradientImage(), "png", new File("gradient_" + filename));
		}
		catch (IOException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
