/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package components;

import javax.swing.JTextArea;

/**
 *
 * @author kendy
 */
public class Logger {

    JTextArea logArea;

    public Logger(JTextArea logArea) {
        this.logArea = logArea;
    }

    public void log(String log) {
        this.logArea.append(log);
        System.out.println(log);
    }
}
