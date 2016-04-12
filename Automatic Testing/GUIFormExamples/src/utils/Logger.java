/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utils;

import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import javax.swing.JTextArea;

/**
 *
 * @author namhb
 */
public class Logger {
    JTextArea logPanel;
    public Logger(JTextArea logPanel)
    {
        this.logPanel = logPanel;
    }
    public void debug(String message)
    {
        String timeStamp = new SimpleDateFormat("yyyyMMdd-HHmmss").format(Calendar.getInstance().getTime());
        message = MessageFormat.format("DEBUG {0}: {1}.", timeStamp, message);
        System.out.println(message);
        this.logPanel.append(message);
        this.logPanel.append("\n");
    }
    public void error(String message)
    {
        String timeStamp = new SimpleDateFormat("yyyyMMdd-HHmmss").format(Calendar.getInstance().getTime());
        message = MessageFormat.format("ERROR {0}: {1}.", timeStamp, message);
        System.out.println(message);
        this.logPanel.append(message);
        this.logPanel.append("\n");
        
    }
}
