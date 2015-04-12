/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package burp;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Label;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.TableModel;

/**
 *
 * @author namhb1
 */
public class Gui extends JPanel{
    public     JPanel  sitePanel, requestPanel;
    public     JPanel  panel1, panel11, panel111;
    public     JPanel  panel12, rightPanel;
    public     JButton buttonHelp;
    public     JTable  proxyTable;
    public Gui()
    {
        initComponents();
    }
    public void initComponents()
    {
        this.setLayout(new BorderLayout());
        
        JPanel topPanel = new JPanel();
        topPanel.setLayout(new BorderLayout());
        //Create SiteMap Tab
        createSiteMap();
        //Options Tab
        JPanel panel2 = new JPanel();

        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.addTab("Site map", panel1);
        tabbedPane.addTab("Options", panel2);

        topPanel.add(tabbedPane, BorderLayout.CENTER);
        this.add(topPanel);
    }
    public void createSiteMap()
    {
        //Panel1, include all
        panel1 = new JPanel(new BorderLayout());
        panel11 = new JPanel(new BorderLayout());
        panel111 = new JPanel(new BorderLayout()); 
        
        //*For Filter on top, top head
        Box topBox = new Box(BoxLayout.LINE_AXIS);
        topBox.add(new Label(" Filter: For example only"));
        topBox.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        panel111.add(topBox, BorderLayout.CENTER);
        buttonHelp = new JButton("Help");
        panel111.add(buttonHelp, BorderLayout.EAST);
        panel111.setBorder(BorderFactory.createEmptyBorder(2, 3, 0, 2));
        panel11.add(panel111,BorderLayout.CENTER);
        
        panel1.add(panel11,BorderLayout.NORTH);
        //Panel include sitemap. proxy, request
        panel12 = new JPanel(new BorderLayout());

        //For sitePanel
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        sitePanel = createSitePanel();
        JScrollPane leftScrollPane = new JScrollPane(sitePanel);
        splitPane.setLeftComponent(leftScrollPane);

        //For left sitePanel
        rightPanel = new JPanel(new BorderLayout());

        //*For rightPanel
        proxyTable = createProxyPanel(); 
        requestPanel = createRequestPanel();
        JScrollPane scrollPane2 = new JScrollPane(proxyTable);
        scrollPane2.setPreferredSize(new Dimension(scrollPane2.getWidth(),250));
        JScrollPane scrollPane3 = new JScrollPane(requestPanel);
        
        JSplitPane splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        splitPane2.setLeftComponent(scrollPane2);
        splitPane2.setRightComponent(scrollPane3);
        rightPanel.add(splitPane2);
        
        //*Add rightPanel
        splitPane.setRightComponent(rightPanel);

        panel12.add(splitPane);

        panel1.add(panel12,BorderLayout.CENTER);
    }
    public JPanel createSitePanel()
    {
        sitePanel = new JPanel(new BorderLayout());
        sitePanel.setPreferredSize(new Dimension(250,sitePanel.getHeight()));
        return sitePanel;
    }
    public JTable createProxyPanel()
    {
        proxyTable = new JTable(dataModel);
        return proxyTable;
    }
    public JPanel createRequestPanel()
    {
        requestPanel = new JPanel(new BorderLayout());
        return requestPanel;
    }
    public TableModel dataModel = new AbstractTableModel() 
    {
        @Override
        public String getColumnName(int columnIndex)
        {
            switch (columnIndex)
            {
                case 0:
                    return "Tool";
                case 1:
                    return "URL";
                default:
                    return "";
            }
        }   
        @Override
        public int getColumnCount() 
        { 
          return 4; 
        }
        @Override
        public int getRowCount() 
        { 
          return 15;
        }
        @Override
        public Object getValueAt(int row, int col) 
        { 
            switch (col)
            {
                case 0:
                    return "";
                case 1:
                    return "";
                default:
                    return "";
            }
        }
    };
}
