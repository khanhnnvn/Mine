package FSM_GRAPH;

import java.util.ArrayList;
import org.apache.james.mime4j.message.Message;
import utils.*;
import java.text.MessageFormat;

public class ThePath {

    ArrayList<ArrayList<Integer>> arrPath;
    public Logger logger;
    public int getSize() {
        return arrPath.size();
    }

    public ThePath(Logger logger) {
        this.logger = logger;
        arrPath = new ArrayList<ArrayList<Integer>>();
    }

    public void Add(ArrayList<Integer> arr) {
        ArrayList<Integer> t = new ArrayList<Integer>();
        for (int i = 0; i < arr.size(); i++) {
            t.add(arr.get(i));
        }
        arrPath.add(t);

    }

    public ArrayList<Integer> getListByIndex(int index) {
        return arrPath.get(index);
    }

    public int getSizeByIndex(int index) {
        return arrPath.get(index).size();
    }

    public int getLastElemFromPathNumber(int index) {
        return arrPath.get(index).get(arrPath.get(index).size() - 1);
    }

    public void sort() {
        for (int i = 0; i < arrPath.size() - 1; i++) {
            for (int j = i + 1; j < arrPath.size(); j++) {
                if (arrPath.get(i).size() > arrPath.get(j).size()) {
                    ArrayList<Integer> t = arrPath.get(i);

                    arrPath.set(i, arrPath.get(j));
                    arrPath.set(j, t);

                }
            }
        }

        for (int i = 0; i < arrPath.size() - 1; i++) {
            for (int j = i + 1; j < arrPath.size(); j++) {
                if (laCon(arrPath.get(i), arrPath.get(j))) {
                    arrPath.remove(i);
                    i = 0;
                    j = 1;
                }
            }
        }
    }

    public boolean laCon(ArrayList<Integer> arr1, ArrayList<Integer> arr2) {
        if (arr1.size() > arr2.size()) {
            return false;
        }
        for (int i = 0; i < arr1.size(); i++) {
            if (arr1.get(i).intValue() != arr2.get(i).intValue()) {
                return false;
            }
        }

        return true;
    }

    public void printPath() {
        for (int i = 0; i < arrPath.size(); i++) {
            String tmp = "";
            ArrayList<Integer> t = arrPath.get(i);
            for (int k = 0; k < t.size(); k++) {
                tmp = MessageFormat.format("{0} {1}", tmp, t.get(k));
            }
            this.logger.debug(MessageFormat.format("{0}. {1}", (i + 1), tmp));
        }
    }

    public void printSomeThingsOfPath() {
        this.logger.debug("About PATH: ");
        for (int i = 0; i < arrPath.size(); i++) {
            this.logger.debug(MessageFormat.format("Size: {0} \tEnd: {1}", getSizeByIndex(i), getLastElemFromPathNumber(i)));
        }
    }

}
