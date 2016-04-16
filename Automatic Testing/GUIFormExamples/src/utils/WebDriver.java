/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utils;

import FSM_GRAPH.FSM;
import components.*;
import htmlElement.*;
import java.text.MessageFormat;
import java.util.ArrayList;
import javax.swing.table.DefaultTableModel;
import utils.*;
import org.openqa.selenium.WebElement;
/**
 *
 * @author kendy
 */
public class WebDriver {
    ListWebElements elemHtmlList = new ListWebElements(); // danh sach cac html element
    ListState stateList = new ListState(); // danh sach cac sate
    ListEvent eventList = new ListEvent(); // danh sach cac event
    ListTransition transitionList = new ListTransition(); // danh sach cac transition
    State beginState = new State();	//trang thai bat dau cua mot SM
    ListState endStateList = new ListState();	//danh sach cac trang thai ket thuc cua mot SM
    Logger logger;
    DefaultTableModel elementmodel, stateModel, transactionModel, eventModel, valueModel;
    FSM fsm;
    Functions functions;
    public WebDriver(Logger logger) {
        this.logger = logger;
        this.functions = new Functions();
    }
    public void import2WebDriver(DefaultTableModel elementmodel, DefaultTableModel stateModel, DefaultTableModel transactionModel, DefaultTableModel eventModel, DefaultTableModel valueModel)
    {
        this.elementmodel = elementmodel;
        this.stateModel = stateModel;
        this.transactionModel = transactionModel;
        this.eventModel = eventModel;
        this.valueModel = valueModel;
        this.importAll();
    }
    public void importAll()
    {
        this.addElement();
        this.addState();
        this.addEvent();
        this.addTransaction();
        this.fsm = new FSM(this.valueModel.getColumnCount() - 2, "test", stateList, transitionList, beginState, endStateList, this.logger);
        ListTransitionSequence transqlist = fsm.getPath_DFS();
        transqlist.printElem();
    }
    public void addElement()
    {
        this.logger.debug("Add from table to Element list");
        int elementRowCount = this.elementmodel.getRowCount();
        int valueColCount = this.valueModel.getColumnCount() - 2;
        for(int i=0; i < elementRowCount; i++)
        {
            String id = this.elementmodel.getValueAt(i, 0).toString();
            String html_id = this.elementmodel.getValueAt(i, 1).toString();
            String type = this.elementmodel.getValueAt(i, 2).toString();
            ArrayList<String> values = new ArrayList<String>();
            for (int j=0; j<valueColCount; j++){
                    String tvalue = this.valueModel.getValueAt(i, j+2).toString();
                    //if (tvalue.length()==0){ Exception e = new Exception(); throw e;} // kiem tra chuan du lieu
                    if (tvalue.length()==0){
                            tvalue = "_";
                    }
                    values.add(tvalue);
            }
        // Add to We
        this.elemHtmlList.addElement(new WebElements(Integer.parseInt(id), html_id, type, values));
        }
        this.logger.debug(MessageFormat.format("Number of element: {0}",this.elemHtmlList.getSize()));
    }
    public void addState()
    {
        this.logger.debug("Add from table to State list");
        int statesCount = this.stateModel.getRowCount();
        int elementRowCount = this.elementmodel.getRowCount();
        for(int i=0; i < statesCount; i++)
        {
            String name = this.stateModel.getValueAt(i, 2).toString();
            int beginEnd = Integer.parseInt(this.stateModel.getValueAt(i, 1).toString());
            int id = Integer.parseInt(this.stateModel.getValueAt(i, 0).toString());
//            System.out.println(type);
            ListElementStatus elemStList = new ListElementStatus();
            for (int j=0; j<elementRowCount; j++){
                if(this.stateModel.getValueAt(i, j+5) != null){
                    String st = this.stateModel.getValueAt(i, j+5).toString();
                    if (st.length() == 0){
                            st = "_";
                    }
                    elemStList.addElement(new ElementStatus(j, st));
                }    
            }
            this.stateList.addState(new State(name, elemStList, this.elemHtmlList));
            if (beginEnd == 0){
                this.beginState = new State(name, elemStList, this.elemHtmlList);
            }else if (beginEnd == 1){
                this.endStateList.addState(new State(name, elemStList, this.elemHtmlList));
            }
        }
        this.logger.debug(MessageFormat.format("Number of states: {0}",this.stateList.getSize()));
    }
    public void addEvent()
    {
        this.logger.debug("Add from event to Event list");
        int eventsCount = this.eventModel.getRowCount();
        for(int i=0; i < eventsCount; i++)
        {
            String name = this.eventModel.getValueAt(i, 1).toString();
            String elem_id, action = "";
            if(this.eventModel.getValueAt(i, 2) != null)
            {
                elem_id = this.eventModel.getValueAt(i, 2).toString();
            }
            else
            {
                elem_id = "";
            }
            if(this.eventModel.getValueAt(i, 3) != null)
            {
                action = this.eventModel.getValueAt(i, 3).toString();
            }
            else
            {
                action = "";
            }
            eventList.addEvent(new Event(name, elem_id, action, elemHtmlList));
        }
        this.logger.debug(MessageFormat.format("Number of events: {0}",this.eventList.getSize()));
    }
    public void addTransaction() {
        this.logger.debug("Add from event to Transaction list");
        int transCount = this.transactionModel.getRowCount();
        int elementRowCount = this.elementmodel.getRowCount();
        for(int i=0; i < transCount; i++)
        {
            for (int j=0; j<elementRowCount; j++){
                String eventNConds;
                if(this.transactionModel.getValueAt(i, j+2) != null)
                {
                    eventNConds = this.transactionModel.getValueAt(i, j+2).toString();
                }
                else
                {
                    eventNConds = "";
                }
                String s1name = this.transactionModel.getValueAt(i, 1).toString();
                String s2name = this.transactionModel.getColumnName(j+2).toString();

                if (eventNConds.length() == 0){
                    eventNConds = "_";
                }
                if(!eventNConds.equals("_"))
                {
                    String eName = this.functions.getNameEvent(eventNConds);
                    this.logger.debug(MessageFormat.format("Name Event:  {0}",eName));
                    Condition cond = this.functions.getCond(eventNConds);
                    transitionList.addTransition(new Transition(eventList.getEventByName(eName), 
                    stateList.getStateByName(s1name), 
                    stateList.getStateByName(s2name), cond));
                }
                
//                ArrayList<String> ECnames = new ArrayList<String>();
//                ECnames = subEvents(eventNConds); //List cac event va condition
//                //System.out.println(s1name + "--" + ename + "-->" + s2name + " :\t" + cellString);
//                for (int k=0 ; k<ECnames.size() ; k++){
//                    if (ECnames.get(k).length()==0 || ECnames.get(k).compareTo("_")==0){
//                    continue;
//                }
//                    String eName = getNameEvent(ECnames.get(k));
//                    Condition cond = getCond(ECnames.get(k));
//                    System.out.println("Name Event: " + eName);
//                    transitionList.addTransition(new Transition(eventList.getEventByName(eName), 
//                        stateList.getStateByName(s1name), 
//                        stateList.getStateByName(s2name), cond));
//                }
            }
        }
        this.logger.debug(MessageFormat.format("Number of transaction: {0}",this.transitionList.getSize()));
    }
    
}
