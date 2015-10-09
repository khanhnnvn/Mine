/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.BurpExtender;
import burp.IBurpExtender;
import burp.IBurpExtenderCallbacks;
import burp.IContextMenuFactory;
import burp.IContextMenuInvocation;
import burp.IExtensionHelpers;
import burp.IHttpRequestResponse;
import burp.IMenuItemHandler;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import javax.swing.JMenu;
import javax.swing.JMenuItem;

/**
 *
 * @author habachnam
 */
public class MenuClick extends JMenu {
    public JMenuItem sqlClick, xssClick, fileClick;
    public IHttpRequestResponse ihrr;
    public IHttpRequestResponse messageinfo;
    public int toolFlag;
    public Gui jPanel1;
    public MenuClick(IHttpRequestResponse ihrr, Gui jPanel1)
    {
        this.ihrr = ihrr;
        this.toolFlag = jPanel1.getLogEntrySize();
        this.jPanel1 = jPanel1;
        this.setText("Send to AWS");
        //Create sub menu
        sqlClick = new  JMenuItem("SQL injection");
        xssClick = new  JMenuItem("Cross Site Scripting");
        fileClick = new  JMenuItem("File Inclusion");
        //Add event
        SQLActionListener sqlAction = new SQLActionListener();
        sqlClick.addActionListener(sqlAction);
        XssActionListener xssAction = new XssActionListener();
        xssClick.addActionListener(xssAction);
        FileActionListener fileAction = new FileActionListener();
        fileClick.addActionListener(fileAction);
        //Add sub menu
        this.add(sqlClick);
        this.add(xssClick);
        this.add(fileClick);
    }
    class SQLActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "SQL injection");
        }
    }
    class XssActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "Cross Site Sripting");
        }
    }
    class FileActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "File Inclusion");
        }
    }
 
}
