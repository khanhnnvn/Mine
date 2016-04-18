/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utils;

import FSM_GRAPH.FSM;
import components.*;
import htmlElement.*;
import java.io.File;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import javax.swing.table.DefaultTableModel;
import utils.*;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.*;

/**
 *
 * @author kendy
 */
public class WebDriverCommand {

    WebDriver driver;
    ListWebElements elemHtmlList = new ListWebElements(); // danh sach cac html element
    ListState stateList = new ListState(); // danh sach cac sate
    ListEvent eventList = new ListEvent(); // danh sach cac event
    ListTransition transitionList = new ListTransition(); // danh sach cac transition
    State beginState = new State();	//trang thai bat dau cua mot SM
    ListState endStateList = new ListState();	//danh sach cac trang thai ket thuc cua mot SM
    Logger logger;
    DefaultTableModel elementmodel, stateModel, transactionModel, eventModel, valueModel, testPathModel;
    FSM fsm;
    Functions functions;

    public WebDriverCommand(Logger logger) {
        this.logger = logger;
        this.functions = new Functions();
    }

    public void import2WebDriver(DefaultTableModel elementmodel, DefaultTableModel stateModel, DefaultTableModel transactionModel, DefaultTableModel eventModel, DefaultTableModel valueModel, DefaultTableModel testPathModel) {
        this.elementmodel = elementmodel;
        this.stateModel = stateModel;
        this.transactionModel = transactionModel;
        this.eventModel = eventModel;
        this.valueModel = valueModel;
        this.testPathModel = testPathModel;
        this.importAll();
    }

    public void importAll() {
        this.logger.debug("Start add to FSM");
        this.addElement();
        this.addState();
        this.addEvent();
        this.addTransaction();
        this.fsm = new FSM(this.valueModel.getColumnCount() - 2, "test", stateList, transitionList, beginState, endStateList, this.logger);
        this.addTestPathTable();
    }

    public void addTestPathTable() {
        int rowID = 1;
        ListTransitionSequence transqlist = fsm.getPath_DFS();
        for (int i = 0; i < transqlist.getSize(); i++) {
            // Print test path detail
            TransitionSequences transq = transqlist.getTransitionByIndex(i);
            this.logger.debug(MessageFormat.format("Test path: {0}", (i + 1)));
            this.logger.debug(transq.getTransitionByIndex(0).getBeginState().getName());
            // Add
            this.testPathModel.addRow(new Object[]{rowID, (i + 1), 0, "", transq.getTransitionByIndex(0).getBeginState().getName(), "", "Begin State"});
            rowID += 1;
            for (int j = 0; j < transq.getSize(); j++) {
                Transition tran = transq.getTransitionByIndex(j);
                Event e = tran.getEvent();
                State s2 = tran.getEndState();
                this.logger.debug("*" + e.name + "=" + s2.name);
                this.testPathModel.addRow(new Object[]{rowID, (i + 1), (j + 1), e.name, s2.name, "Pending", ""});
                // Set id to remember
                tran.setTableID(rowID-1);
                rowID += 1;
            }
        }
    }

    public void addElement() {
        this.logger.debug("Add from table to Element list");
        int elementRowCount = this.elementmodel.getRowCount();
        int valueColCount = this.valueModel.getColumnCount() - 2;
        for (int i = 0; i < elementRowCount; i++) {
            String id = this.elementmodel.getValueAt(i, 0).toString();
            String html_id = this.elementmodel.getValueAt(i, 1).toString();
            String type = this.elementmodel.getValueAt(i, 2).toString();
            ArrayList<String> values = new ArrayList<String>();
            for (int j = 0; j < valueColCount; j++) {
                String tvalue = this.valueModel.getValueAt(i, j + 2).toString();
                //if (tvalue.length()==0){ Exception e = new Exception(); throw e;} // kiem tra chuan du lieu
                if (tvalue.length() == 0) {
                    tvalue = "_";
                }
                values.add(tvalue);
            }
            // Add to We
            this.elemHtmlList.addElement(new WebElements(Integer.parseInt(id), html_id, type, values));
        }
        this.logger.debug(MessageFormat.format("Number of element: {0}", this.elemHtmlList.getSize()));
    }

    public void addState() {
        this.logger.debug("Add from table to State list");
        int statesCount = this.stateModel.getRowCount();
        int elementRowCount = this.elementmodel.getRowCount();
        for (int i = 0; i < statesCount; i++) {
            String name = this.stateModel.getValueAt(i, 2).toString();
            int beginEnd = Integer.parseInt(this.stateModel.getValueAt(i, 1).toString());
            int id = Integer.parseInt(this.stateModel.getValueAt(i, 0).toString());
            ListElementStatus elemStList = new ListElementStatus();
            for (int j = 0; j < elementRowCount; j++) {
                if (this.stateModel.getValueAt(i, j + 5) != null) {
                    String st = this.stateModel.getValueAt(i, j + 5).toString();
                    if (st.length() == 0) {
                        st = "_";
                    }
                    elemStList.addElement(new ElementStatus(j, st));
                }
            }
            this.stateList.addState(new State(name, elemStList, this.elemHtmlList));
            if (beginEnd == 0) {
                this.beginState = new State(name, elemStList, this.elemHtmlList);
            } else if (beginEnd == 1) {
                this.endStateList.addState(new State(name, elemStList, this.elemHtmlList));
            }
        }
        this.logger.debug(MessageFormat.format("Number of states: {0}", this.stateList.getSize()));
    }

    public void addEvent() {
        this.logger.debug("Add from event to Event list");
        int eventsCount = this.eventModel.getRowCount();
        for (int i = 0; i < eventsCount; i++) {
            String name = this.eventModel.getValueAt(i, 1).toString();
            String elem_id, action = "";
            if (this.eventModel.getValueAt(i, 2) != null) {
                elem_id = this.eventModel.getValueAt(i, 2).toString();
            } else {
                elem_id = "";
            }
            if (this.eventModel.getValueAt(i, 3) != null) {
                action = this.eventModel.getValueAt(i, 3).toString();
            } else {
                action = "";
            }
            eventList.addEvent(new Event(name, elem_id, action, elemHtmlList));
        }
        this.logger.debug(MessageFormat.format("Number of events: {0}", this.eventList.getSize()));
    }

    public void addTransaction() {
        this.logger.debug("Add from event to Transaction list");
        int transCount = this.transactionModel.getRowCount();
        for (int i = 0; i < transCount; i++) {
            for (int j = 0; j < transCount; j++) {
                String eventNConds;
                if (this.transactionModel.getValueAt(i, j + 2) != null) {
                    eventNConds = this.transactionModel.getValueAt(i, j + 2).toString();
                } else {
                    eventNConds = "";
                }
                String s1name = this.transactionModel.getValueAt(i, 1).toString();
                String s2name = this.transactionModel.getColumnName(j + 2).toString();

                if (eventNConds.length() == 0) {
                    eventNConds = "_";
                }
                if (!eventNConds.equals("_")) {
                    String eName = this.functions.getNameEvent(eventNConds);
                    this.logger.debug(MessageFormat.format("Name Event:  {0}", eName));
                    Condition cond = this.functions.getCond(eventNConds);
                    transitionList.addTransition(new Transition(eventList.getEventByName(eName),
                            stateList.getStateByName(s1name),
                            stateList.getStateByName(s2name), cond));
                }
            }
        }
        this.logger.debug(MessageFormat.format("Number of transaction: {0}", this.transitionList.getSize()));
    }

    public void startFirefox() {
        File pathToBinary = new File("D:\\03.Portable\\FirefoxPortable\\App\\Firefox\\firefox.exe");
        FirefoxBinary ffBinary = new FirefoxBinary(pathToBinary);
        FirefoxProfile firefoxProfile = new FirefoxProfile();
        this.driver = new FirefoxDriver(ffBinary, firefoxProfile);
        this.driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }

    public void runAllTestCase(String startURL) {
        ListTransitionSequence transqlist = fsm.getPath_DFS();
        for (int i = 0; i < transqlist.getSize(); i++) {
            TransitionSequences transq = transqlist.getTransitionByIndex(i);
            // Run test case
            this.runOneTransitionSequences(startURL, transq, i);
        }
    }

    public void runOneTransitionSequences(String startURL, TransitionSequences transq, int test_c) {
        boolean passone = true;
        this.driver.get(startURL);
        // Check delete cookie
        this.driver.manage().deleteAllCookies();
        // Check begin state
        for (int j = 0; j < transq.getSize(); j++) {
            Transition tran = transq.getTransitionByIndex(j);
            Event e = tran.getEvent();
            State s1 = tran.getBeginState();
            State s2 = tran.getEndState();
            // Don`t know
            // Check state
            // And do cond if need
            int reasonCol = 6;
            int statusCol = 5;
            this.logger.debug(MessageFormat.format("{0}: {1}*{2}={3}", (j + 1), s1.getName(), e.getName(), s2.getName()));
            if (!tran.changeTrans(driver, test_c)) {
                this.logger.debug("FAIL");
                break;
            }
            try {
                e.doEvent(driver, test_c, this.logger);
            } catch (Exception err) {
                passone = false;
                this.logger.debug("FAIL EVENT");
                this.testPathModel.setValueAt("FAIL EVENT", tran.getTableID(), reasonCol);
            }
            // check state sau do
            if (!s2.checkState(driver, test_c, this.logger)) {
                passone = false;
                this.logger.debug(MessageFormat.format("FAIL STATE: {0}", s2.getName()));
                this.testPathModel.setValueAt("FAIL STATE", tran.getTableID(), reasonCol);
                break;
            }
            // Update to TestPath table    
            if(passone) this.testPathModel.setValueAt("OK", tran.getTableID(), statusCol);
                    else this.testPathModel.setValueAt("FAIL", tran.getTableID(), statusCol);
        }

    }

}
