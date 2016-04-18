package components;

import htmlElement.ListWebElements;
import htmlElement.ElementStatus;
import htmlElement.ListElementStatus;
import htmlElement.WebElements;
import org.openqa.selenium.WebDriver;
import arg.*;
import java.text.MessageFormat;

public class Transition {

    public Event event;
    public State beginState;
    public State endState;
    public Condition transCond;
    public int tableID;

    public Transition(Event e, State s1, State s2, Condition c) {
        beginState = s1;
        endState = s2;
        event = e;
        transCond = c;
    }

    public void setTableID(int id) {
        this.tableID = id;
    }

    public int getTableID() {
        return this.tableID;
    }

    public boolean changeTrans(WebDriver driver, int test_case) {
        try {
            boolean test = true;
            ListWebElements listWebElements = beginState.listWebElements;
            ListElementStatus listElementStatus = beginState.listElementStatus;
            for (int i = 0; i < listElementStatus.getSize(); i++) {
                ElementStatus elementStatus = listElementStatus.getElementByIndex(i);
                if (elementStatus.getStatus().compareTo(ElementStatusValue.IGNORE) == 0) {
                    continue;
                }

                WebElements eh = listWebElements.getElementById(elementStatus.getId());
                if (eh.getValueAt(test_case).compareTo(ElementStatusValue.IGNORE) == 0) {
                    continue;
                }

                // Check [guard] trong moi transition de biet trans do co thuc hien dc ko
                if (transCond.getHtml_id() == null) {
                    test = true;
                } else {
                    String value_tc = eh.getValueAt(transCond.getHtml_id(), test_case);
                    if (value_tc != null) {
                        if (transCond.getHtml_id().equals(eh.getHtml_id())) {
                            if (!transCond.getValues().equals(value_tc)) {
                                test = false;
                            } else {
                                test = true;
                            }
                        }
                    }
                }
            }

            return test;
        } catch (Exception e) {
            e.printStackTrace();
            return true;
        }
    }

    //Getter & Setter
    public String getName() {
        return event.getName();
    }

    public State getBeginState() {
        return beginState;
    }

    public State getEndState() {
        return endState;
    }

    public Event getEvent() {
        return event;
    }

    public void setNameEndState(String name) {
        endState.setName(name);
    }

    public void setNameEvent(String name) {
        event.setName(name);
    }

    public String logTrans(utils.Logger logger) {
        String trans = (MessageFormat.format("{0} ----> {1}", beginState.getName(), endState.getName()));
        logger.debug(trans);
        return trans;
    }

    public void printTrans(utils.Logger logger) {
        String trans = (MessageFormat.format("{0} ---- {1} ----> {2}", beginState.getName(), event.getName(), endState.getName()));
        logger.debug(trans);
    }
}
