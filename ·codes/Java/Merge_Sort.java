public class Merge_Sort {
    /**
     * Merge Sort for int[n]
     */
    private int[] ints;

    public Merge_Sort(int[] ints, int n) {
        this.ints = Sort_int(ints, n);
    }

    public int[] getInts() {
        return ints;
    }

    public static int[] Sort_int(int[] ints, int n) {
        if (n > 1) {
            int p = n / 2;
            int[] ints1 = new int[p];
            int[] ints2 = new int[n - p];
            for (int i = 0; i < n; i++) {
                if (i < p) ints1[i] = ints[i];
                else ints2[i - p] = ints[i];
            }
            ints1 = Sort_int(ints1, p);
            ints2 = Sort_int(ints2, n - p);
            ints = Merge_int(ints1, ints2, p, n - p);
        }
        return ints;
    }

    public static int[] Merge_int(int[] ints1, int[] ints2, int n1, int n2) {
        int n = n1 + n2;
        int[] ints = new int[n];
        int i = 0, j = 0;
        for (int k = 0; k < n; k++) {
            if (i < n1 && (j >= n2 || ints1[i] <= ints2[j])) {
                ints[k] = ints1[i];
                i++;
            } else {
                ints[k] = ints2[j];
                j++;
            }
        }
        return ints;
    }

    /**
     * Merge Sort for long[n]
    */
    private long[] longs;

    public Merge_Sort(long[] longs, int n) {
        this.longs = Sort_long(longs, n);
    }

    public long[] getLongs() {
        return longs;
    }

    public static long[] Sort_long(long[] longs, int n) {
        if (n > 1) {
            int p = n / 2;
            long[] longs1 = new long[p];
            long[] longs2 = new long[n - p];
            for (int i = 0; i < n; i++) {
                if (i < p) longs1[i] = longs[i];
                else longs2[i - p] = longs[i];
            }
            longs1 = Sort_long(longs1, p);
            longs2 = Sort_long(longs2, n - p);
            longs = Merge_long(longs1, longs2, p, n - p);
        }
        return longs;
    }

    public static long[] Merge_long(long[] longs1, long[] longs2, int n1, int n2) {
        int n = n1 + n2;
        long[] longs = new long[n];
        int i = 0, j = 0;
        for (int k = 0; k < n; k++) {
            if (i < n1 && (j >= n2 || longs1[i] <= longs2[j])) {
                longs[k] = longs1[i];
                i++;
            } else {
                longs[k] = longs2[j];
                j++;
            }
        }
        return longs;
    }
}
