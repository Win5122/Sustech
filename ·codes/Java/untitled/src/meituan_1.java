import java.util.Scanner;

public class meituan_1 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int t = input.nextInt();
        for (int i = 0; i < t; i++) {
            int n = input.nextInt();
            int[] array = new int[n];
            int dis_max = 0, count = 0;
            for (int j = 0; j < n; j++) {
                array[j] = input.nextInt();
                dis_max += array[j];
                if (array[j] == 1) {
                    count++;
                }
            }
            int x = input.nextInt();
            int y = input.nextInt();
            int p = input.nextInt();
            int q = input.nextInt();
            int dis_x = Math.abs(x - p);
            int dis_y = Math.abs(y - q);
            int dis_all = dis_x + dis_y;
            int dis_min = (count % 2 == 0) ? 0 : 1;
            if ((dis_max - dis_all) % 2 != 0) {
                System.out.println("NO");
                continue;
            }
            if (dis_all < dis_x || dis_all < dis_y || dis_all < dis_max) {
                System.out.println("NO");
                continue;
            }
            if (dis_min > dis_all) {
                System.out.println("NO");
                continue;
            }
            System.out.println("YES");
        }
    }
}