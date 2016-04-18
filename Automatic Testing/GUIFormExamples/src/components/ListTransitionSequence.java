package components;

import java.text.MessageFormat;
import java.util.ArrayList;
import javax.xml.soap.MessageFactory;

public class ListTransitionSequence {

    ArrayList<TransitionSequences> listTranSq;

    public ListTransitionSequence() {
        listTranSq = new ArrayList<TransitionSequences>();
    }

    public void addTransitionsq(TransitionSequences _tranSq) {
        listTranSq.add(_tranSq);
    }

    public TransitionSequences getTransitionByIndex(int i) {
        return listTranSq.get(i);
    }

    public int getSize() {
        return listTranSq.size();
    }

    public void removeTransq(int i) {
        listTranSq.remove(i);
    }

    public void removeTransq(TransitionSequences transq) {
        listTranSq.remove(transq);
    }

    public String logElems(utils.Logger logger) {
        String result = "";
        result += "Number of Transition Sequence: " + getSize() + "\n";

        for (int i = 0; i < getSize(); i++) {
            System.out.println("Transition Sequence " + i + " - " + listTranSq.get(i).getSize() + ":");
            result += "Transition Sequence " + (i + 1) + " - " + listTranSq.get(i).getSize() + ":\n";
            result += listTranSq.get(i).logTransq(logger);
        }

        return result;
    }

    public void printElem(utils.Logger logger) {
        logger.debug(MessageFormat.format("Number of Transition Sequence: {0}", getSize()));
        for (int i = 0; i < getSize(); i++) {
            logger.debug(MessageFormat.format("Transition Sequence {0} - {1}:", i, listTranSq.get(i).getSize()));
            listTranSq.get(i).printTransq(logger);
        }
    }

}
