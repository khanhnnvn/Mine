/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.BurpExtender;
import burp.IBurpExtenderCallbacks;
import burp.IExtensionHelpers;
import burp.IHttpRequestResponse;
import burp.IMessageEditor;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Label;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

/**
 *
 * @author namhb1
 */
public class Gui extends JPanel{
    public      JPanel  sitePanel, requestPanel;
    public      JPanel  panel1, panel11, panel111;
    public      JPanel  panel12, rightPanel;
    public      JPanel  resultAWS, debugLog;
    public      JButton buttonHelp;
    public      JTable  proxyTable;
    public      BurpExtender BurpExtender;
    public      DefaultTableModel dataModel;
    public      JPanel topPanel, panel2, requestInfoPanel, responseInfoPanel;
    public  final   List<LogEntry> log = new ArrayList<LogEntry>();
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    private IMessageEditor requestViewer;
    private IMessageEditor responseViewer;
    public CheckAWS checkAWSProcess;
    public int timeToCheck;
    
    public Gui(BurpExtender BurpExtender)
    {
        this.BurpExtender = BurpExtender;
        this.callbacks = BurpExtender.callbacks;
        this.helpers = BurpExtender.helpers;
        initComponents();
        timeToCheck = 1000;
        checkAWSProcess = new CheckAWS("Check AWS");
        checkAWSProcess.start();
    }
    public void initComponents()
    {
        this.setLayout(new BorderLayout());
        
        topPanel = new JPanel();
        topPanel.setLayout(new BorderLayout());
        //Create SiteMap Tab
        createSiteMap();
        //Options Tab
        panel2 = new JPanel();

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
        splitPane.setDividerSize(3);
        sitePanel = createSitePanel();
        JScrollPane leftScrollPane = new JScrollPane(sitePanel);
        splitPane.setLeftComponent(leftScrollPane);

        //For left sitePanel
        rightPanel = new JPanel(new BorderLayout());

        //*For rightPanel
        proxyTable = createProxyPanel(); 
        requestPanel = createRequestPanel();
        JScrollPane scrollPane2 = new JScrollPane(proxyTable);
        scrollPane2.setPreferredSize(new Dimension(scrollPane2.getWidth(),230));
        //JScrollPane scrollPane3 = new JScrollPane(requestPanel);
        
        JSplitPane splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        splitPane2.setDividerSize(3);
        splitPane2.setLeftComponent(scrollPane2);
        splitPane2.setRightComponent(requestPanel);
        rightPanel.add(splitPane2);
        
        //*Add rightPanel
        splitPane.setRightComponent(rightPanel);

        panel12.add(splitPane);

        panel1.add(panel12,BorderLayout.CENTER);
    }
    public JPanel createSitePanel()
    {
        sitePanel = new JPanel(new BorderLayout());
        sitePanel.setPreferredSize(new Dimension(300,sitePanel.getHeight()));
        return sitePanel;
    }
    public JTable createProxyPanel()
    {
        dataModel = new DefaultTableModel();
        dataModel.addColumn("#");
        dataModel.addColumn("Status");
        dataModel.addColumn("Method");
        dataModel.addColumn("Profile");
        dataModel.addColumn("URL");
        dataModel.addColumn("Added Time");
        proxyTable = new JTable(dataModel);
        proxyTable.getColumnModel().getColumn(0).setMaxWidth(50);
        proxyTable.getColumnModel().getColumn(1).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(2).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(3).setMaxWidth(300);
        proxyTable.getColumnModel().getColumn(5).setMaxWidth(100);
        proxyTable.addMouseListener(new MouseAdapter() 
            {
                public void mouseClicked(MouseEvent e)
                {
                    int row = proxyTable.getSelectedRow();
                    LogEntry logEntry = log.get(row);
                    requestViewer.setMessage(logEntry.requestResponse.getRequest(), true);
                    responseViewer.setMessage(logEntry.requestResponse.getResponse(), false);
                }
            });
        return proxyTable;
    }
    public int getLogEntrySize()
    {
        return log.size();
    }
    public void addRowDataModel(int tool, IHttpRequestResponse messageInfo, String check)
    {
        URL url = helpers.analyzeRequest(messageInfo).getUrl();
        String method = helpers.analyzeRequest(messageInfo).getMethod();
        String path = url.getPath().toString();
        Date now = new Date();
        SimpleDateFormat ft = new SimpleDateFormat ("HH:mm");
        dataModel.addRow(new Object[] { 
            tool,
            "Pending",
            method,
            check,
            url.getPath().toString(),
            ft.format(now)
        });
        log.add(new LogEntry(tool, callbacks.saveBuffersToTempFiles(messageInfo), url, check, now));
    }
    public JPanel createRequestPanel()
    {
        requestPanel = new JPanel(new BorderLayout());
        
        //create tab

        JTabbedPane tabbedRequestResponsePane = new JTabbedPane();
        requestViewer = callbacks.createMessageEditor(BurpExtender, false);
        responseViewer = callbacks.createMessageEditor(BurpExtender, false);
        tabbedRequestResponsePane.addTab("Request", requestViewer.getComponent());
        tabbedRequestResponsePane.addTab("Response", responseViewer.getComponent());
        resultAWS = createResultAWSTab();
        tabbedRequestResponsePane.addTab("AWS Scanner", resultAWS);
        int count = tabbedRequestResponsePane.getTabCount();
        tabbedRequestResponsePane.setSelectedIndex(count-1);
        debugLog = creatDebugLogTab();
        tabbedRequestResponsePane.addTab("Debug Log", debugLog);
        requestPanel.add(tabbedRequestResponsePane, BorderLayout.CENTER);
        return requestPanel;
    }
    public JPanel createResultAWSTab()
    {
        JPanel resultAWS2 = new JPanel();
        return resultAWS2;
    }
    public JPanel creatDebugLogTab()
    {
        JPanel debugTab = new JPanel();
        return debugTab;
    }
    public List<LogEntry> getPending()
    {
        List<LogEntry> logPending = log.stream().filter(u -> u.status.startsWith("Pending")).collect(Collectors.toList());
        return logPending;
    }
    class CheckAWS implements Runnable
    {
        private Thread t;
        private String threadName;

        CheckAWS( String name)
        {
            threadName = name;
            System.out.println("Creating " +  threadName );
        }
        @Override
        public void run() {
            try
            {
                while(true)
                {
                    //Process check log entry array pending to scan
                    //Get pending
                    List<LogEntry> penddingList = getPending();
                    if(penddingList.size() > 0)
                    {
                        //Sort

                    }
                    // size < 0, nothing to do
                    Thread.sleep(timeToCheck);
                }
            }
            catch(Exception e)
            {
                System.out.println(e.toString());
            }
        }
        public void start()
        {
            if (t == null)
            {
                t = new Thread(this, threadName);
                t.start();
            }
        }
        
    }
}
