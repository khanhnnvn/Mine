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
import burp.IHttpRequestResponsePersisted;
import burp.IMessageEditor;
import burp.IRequestInfo;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
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
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextPane;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
/**
 *
 * @author namhb1
 */
public class Gui extends JPanel{
    public      Label   labelStatusAll;
    public      JPanel  sitePanel, requestPanel;
    public      JPanel  panel1, panel11, panel111;
    public      JPanel  panel12, rightPanel;
    public      JPanel  resultAWS, debugLog;
    public      JPanel  optionTabs;
    public      JButton buttonHelp;
    public      JTable  proxyTable;
    public      BurpExtender BurpExtender;
    public      DefaultTableModel dataModel;
    public      JPanel topPanel, panel2, requestInfoPanel, responseInfoPanel;
    public      JTextArea debugText;
    public  final   List<LogEntry> log = new ArrayList<LogEntry>();
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    private IMessageEditor requestViewer;
    private IMessageEditor responseViewer;
    public CheckAWS checkAWSProcess;
    public int timeToCheck;
    public Aws aws;
    public boolean scanning=false;
    SimpleDateFormat ft = new SimpleDateFormat ("HH:mm");
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
        createOptionTab();

        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.addTab("AWV Scanner", panel1);
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
        labelStatusAll = new Label("   0 request, 0 pendding, 0 scanned");
        topBox.add(labelStatusAll);
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
        dataModel.addColumn("^ ^");
        dataModel.addColumn("Method");
        dataModel.addColumn("Profile");
        dataModel.addColumn("URL");
        dataModel.addColumn("Added");
        dataModel.addColumn("Finish");
        dataModel.addColumn("High");
        dataModel.addColumn("Medium");
        dataModel.addColumn("Low");
        dataModel.addColumn("Info");
        
        proxyTable = new JTable(dataModel);
        //Before
        proxyTable.getColumnModel().getColumn(0).setMaxWidth(50);
        proxyTable.getColumnModel().getColumn(1).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(2).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(3).setMaxWidth(300);
        proxyTable.getColumnModel().getColumn(4).setMaxWidth(100);
        //URL
        //After
        proxyTable.getColumnModel().getColumn(6).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(7).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(8).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(9).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(10).setMaxWidth(100);
        proxyTable.getColumnModel().getColumn(11).setMaxWidth(100);

                
        proxyTable.addMouseListener(new MouseAdapter() 
            {
                public void mouseClicked(MouseEvent e)
                {
                    int row = proxyTable.getSelectedRow();
                    LogEntry logEntry = log.get(row);
                    requestViewer.setMessage(logEntry.requestResponse.getRequest(), true);
                    responseViewer.setMessage(logEntry.requestResponse.getResponse(), false);
                    debugText.setText(logEntry.debugLog);
                }
            });
        return proxyTable;
    }
    public int getLogEntrySize()
    {
        return log.size();
    }
    public int getLogEntryPending()
    {
        return getPending().size();
    }
    public int getLogEntryScanned()
    {
        return getScanned().size();
    }
    public void addRowDataModel(int tool, IHttpRequestResponse messageInfo, String check)
    {
        URL url = helpers.analyzeRequest(messageInfo).getUrl();
        String method = helpers.analyzeRequest(messageInfo).getMethod();
        String path = url.getPath().toString();
        Date now = new Date();
        
        dataModel.addRow(new Object[] { 
            tool,
            "Pending",
            "No",
            method,
            check,
            url.getPath().toString(),
            ft.format(now),
            null,
            0,
            0,
            0,
            0
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
        JPanel debugTab = new JPanel(new BorderLayout());
        debugText = new JTextArea();
        JScrollPane scrollPane3 = new JScrollPane(debugText);
        debugTab.add(scrollPane3, BorderLayout.CENTER);
        return debugTab;
    }
    public void updateStatus(LogEntry logEntry, String status)
    {
        int row = log.indexOf(logEntry);
        logEntry.status = status;
        proxyTable.setValueAt(status, row, 1);
    }
    public void updatevulnerability(LogEntry logEntry, int level)
    {
        int row = log.indexOf(logEntry);
        //High
        if(level == 1)
        {
            logEntry.high = logEntry.high + 1;
            proxyTable.setValueAt(logEntry.high, row, 8);
            logEntry.hackable = "Yes";
            proxyTable.setValueAt(logEntry.hackable, row, 2);
        }
        //Medium
        if(level == 2)
        {
            logEntry.medium = logEntry.medium + 1;
            proxyTable.setValueAt(logEntry.medium, row, 9);
        }
        //Low
        if(level == 3)
        {
            logEntry.low = logEntry.low + 1;
            proxyTable.setValueAt(logEntry.low, row, 10);
        }
        //Info
        if(level == 4)
        {
            logEntry.info = logEntry.info + 1;
            proxyTable.setValueAt(logEntry.info, row, 11);
        }
    }
    public void addDebugLog(LogEntry logEntry, String str)
    {
        logEntry.debugLog = logEntry.debugLog + "\n" + str;
    }
    public List<LogEntry> getPending()
    {
        List<LogEntry> logPending = log.stream().filter(u -> u.status.startsWith("Pending")).collect(Collectors.toList());
        return logPending;
    }
    public List<LogEntry> getScanned()
    {
        List<LogEntry> logPending = log.stream().filter(u -> u.status.startsWith("Scanned")).collect(Collectors.toList());
        return logPending;
    }
    public void startScan(LogEntry logEntry)
    {
        IHttpRequestResponsePersisted messageInfo = logEntry.requestResponse;
        IRequestInfo reqInfo = this.helpers.analyzeRequest(messageInfo);
        String url = reqInfo.getUrl().toString();
        aws = new Aws(callbacks, helpers, url, logEntry, this);
        aws.saveFile(messageInfo);
    }
    public void createOptionTab()
    {
        panel2 = new JPanel(new BorderLayout());
        
        JPanel panel21 = new JPanel(new BorderLayout());
        JPanel panel211 = new JPanel(new BorderLayout());
        
        Box allBox = new Box(BoxLayout.LINE_AXIS);
        JPanel optionPanel = new JPanel(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        //c.fill = GridBagConstraints.HORIZONTAL;
        c.anchor = GridBagConstraints.WEST;
        JTextPane   stt1 = new JTextPane();
        stt1.setBorder(new EmptyBorder(0, 10, 0, 0));
        stt1.setContentType("text/html");
        stt1.setText("<html><h2><font color=\"#E58900\">Acunetix Web Vunlerabilitity Configuration</font></h2></html>");
        c.gridx = 0;
        c.gridy = 0; 
        optionPanel.add(stt1, c);
        
        allBox.add(optionPanel);
        allBox.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        
        panel211.add(allBox, BorderLayout.CENTER );
        panel21.add(panel211, BorderLayout.CENTER );
        panel2.add(panel21, BorderLayout.NORTH);
    }
    class CheckAWS implements Runnable
    {
        private Thread t;
        private String threadName;

        CheckAWS( String name)
        {
            threadName = name;
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
                        LogEntry logEntry = penddingList.stream().findFirst().get();
                        
                        //Send to AWS
                        //Create one process
                        StartScan startAWSScan = new StartScan("StartScan", logEntry);
                        startAWSScan.start();
                        
                    }
                    // size < 0, nothing to do
                    //Update labelStatusAll
                    int allLog = getLogEntrySize();
                    int penLog = getLogEntryPending();
                    int scaLog = getLogEntryScanned();
                    String strLog = String.format("   %d request, %d pendding, %d scanned", allLog, penLog, scaLog);
                    labelStatusAll.setText(strLog);
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
    class StartScan implements Runnable
    {
        private Thread t;
        private String threadName;
        public LogEntry logEntry;

        StartScan(String name, LogEntry logEntry)
        {
            threadName = name;
            this.logEntry = logEntry;
        }

        @Override
        public void run() {
            try
            {
                //Start Scan, check lock before scan
                if(!scanning)
                {
                    scanning = true;
                    startScan(logEntry);
                    //Update
                    Date now = new Date();
                    proxyTable.setValueAt("Scanned", logEntry.tool, 1);
                    proxyTable.setValueAt(ft.format(now), logEntry.tool, 7);
                    logEntry.status = "Scanned";
                    logEntry.finishTime = now;
                    scanning = false;
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
