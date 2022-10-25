package seamcarving.seamfinding;

import seamcarving.Picture;
import seamcarving.SeamCarver;
import seamcarving.energy.EnergyFunction;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Dynamic programming implementation of the {@link SeamFinder} interface.
 *
 * @see SeamFinder
 * @see SeamCarver
 */
public class DynamicProgrammingSeamFinder implements SeamFinder {

    @Override
    public List<Integer> findHorizontal(Picture picture, EnergyFunction f) {
        double[][] energyCost = new double[picture.width()][picture.height()];
        List<Integer> shortestPath = new ArrayList<>();
        for (int i = 0; i < picture.height(); i++) {
            energyCost[0][i] = f.apply(picture, 0, i);
        }
        for (int i = 1; i < picture.width(); i++) {
            energyCost[i][0] = f.apply(picture, i, 0) + Math.min(energyCost[i - 1][0], energyCost[i - 1][1]);
            for (int j = 1; j < picture.height() - 1; j++) {
                energyCost[i][j] = f.apply(picture, i, j) + Math.min(Math.min(energyCost[i - 1][j - 1], energyCost[i - 1][j]), energyCost[i - 1][j + 1]);
            }
            energyCost[i][picture.height() - 1] = f.apply(picture, i, picture.height() - 1) + Math.min(energyCost[i - 1][picture.height() - 2], energyCost[i - 1][picture.height() - 1]);
        }
        double smallNum = energyCost[picture.width() - 1][0];
        int index = 0;
        for (int j = 1; j < picture.height(); j ++) {
            if (energyCost[picture.width() - 1][j] < smallNum) {
                index = j;
                smallNum = energyCost[picture.width() - 1][j];
            }
        }
        shortestPath.add(index);
        int temp;
        for (int i = picture.width() - 2; i >= 0; i--) {
            if (index - 1 >= 0) {
                smallNum = energyCost[i][index - 1];
                temp = index - 1;
            } else {
                smallNum = energyCost[i][index];
                temp = index;
            }
            for (int j = 0; j < 2; j++) {
                if (index + j < picture.height() && energyCost[i][index + j] < smallNum) {
                    smallNum = energyCost[i][index + j];
                    temp = index +j;
                }
            }
            index = temp;
            shortestPath.add(index);
        }
        Collections.reverse(shortestPath);
        return shortestPath;
    }
}