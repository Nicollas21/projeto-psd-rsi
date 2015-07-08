package br.com.rabbit.storm;

import static com.googlecode.charts4j.Color.BLACK;
import static com.googlecode.charts4j.Color.RED;
import static com.googlecode.charts4j.Color.YELLOW;
import static com.googlecode.charts4j.UrlUtil.normalize;
import static org.junit.Assert.assertEquals;

import java.util.logging.Level;
import java.util.logging.Logger;

import org.junit.BeforeClass;
import org.junit.Test;

import com.googlecode.charts4j.Color;
import com.googlecode.charts4j.GCharts;
import com.googlecode.charts4j.PieChart;
import com.googlecode.charts4j.Slice;

/**
 *
 * @author Julien Chastang (julien.c.chastang at gmail dot com)
 */
public class PieChartExample {

    @BeforeClass
    public static void setUpBeforeClass() throws Exception {
        Logger.global.setLevel(Level.ALL);
    }

    @Test
    public void example1() {
        // EXAMPLE CODE START
        Slice s1 = Slice.newSlice(60, Color.newColor("CACACA"), "Safari", "Apple");
        Slice s2 = Slice.newSlice(40, Color.newColor("DF7417"), "Firefox", "Mozilla");
        //Slice s3 = Slice.newSlice(30, Color.newColor("951800"), "Chrome", "Google");
        //Slice s4 = Slice.newSlice(10, Color.newColor("01A1DB"), "Internet Explorer", "Microsoft");

        PieChart chart = GCharts.newPieChart(s1, s2);
        chart.setTitle("A Better Web", BLACK, 16);
        chart.setSize(500, 200);
        chart.setThreeD(true);
        String url = chart.toURLString();
        // EXAMPLE CODE END. Use this url string in your web or
        // Internet application.
        Logger.global.info(url);
        String expectedString = "http://chart.apis.google.com/chart?cht=p3&chs=500x200&chts=000000,16&chd=e:TNTNTNGa&chtt=A+Better+Web&chco=CACACA,DF7417,951800,01A1DB&chdl=Apple|Mozilla|Google|Microsoft&chl=Safari|Firefox|Chrome|Internet+Explorer";
        assertEquals("Junit error", normalize(expectedString), normalize(url));
    }

    @Test
    public void example2() {
        // EXAMPLE CODE START
        Slice s1 = Slice.newSlice(90, YELLOW, "Ms. Pac-Man");
        Slice s2 = Slice.newSlice(10, RED, "Red Lips");

        PieChart chart = GCharts.newPieChart(s1, s2);
        chart.setTitle("2D Pie Chart", BLACK, 16);
        chart.setSize(500, 200);
        String url = chart.toURLString();
        // EXAMPLE CODE END. Use this url string in your web or
        // Internet application.
        Logger.global.info(url);
        String expectedString = "http://chart.apis.google.com/chart?chco=FFFF00,FF0000&chd=e:5mGa&chl=Ms.+Pac-Man|Red+Lips&chs=500x200&cht=p&chts=000000,16&chtt=2D+Pie+Chart";
        assertEquals("Junit error", normalize(expectedString), normalize(url));
    }

}
