package components;

import java.text.MessageFormat;
import java.util.ArrayList;
import utils.*;
public class ListState {

    ArrayList<State> listStates;
    Logger logger;
    public ListState() {
        listStates = new ArrayList<State>();
    }

    public void addState(State _state) {
        listStates.add(_state);
    }

    public State getStateByIndex(int index) {
        return listStates.get(index);
    }

    public boolean checkExist(String _name) {
        for (int i = 0; i < listStates.size(); i++) {
            if (listStates.get(i).getName().equals(_name)) {
                return true;
            }
        }
        return false;
    }

    public State getStateByName(String _name) {
        for (int i = 0; i < listStates.size(); i++) {
            if (listStates.get(i).getName().compareTo(_name) == 0) {
                return listStates.get(i);
            }
        }
        return null;
    }

    public int getSize() {
        return listStates.size();
    }

    public void removeStateByName(String name) {
        State temp = getStateByName(name);
        if (temp != null) {
            listStates.remove(temp);
        }
    }

    public void printStateDetail(utils.Logger logger) {
        for (int i = 0; i < listStates.size(); i++) {
            listStates.get(i).printState(logger);
        }
    }

    public void printStateList(utils.Logger logger) {
        for (int i = 0; i < listStates.size(); i++) {
            listStates.get(i).setId(i);
            logger.debug(MessageFormat.format("{0}/{1}", listStates.get(i).id, listStates.get(i).name));
        }
    }
}
