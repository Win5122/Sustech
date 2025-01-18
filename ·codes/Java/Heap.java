class Heap {
    int[] heap;
    int size = 0;

    public Heap(int n) {
        heap = new int[n + 1];
    }

    public void insert_Big(int x) {
        heap[++size] = x;
        int index = size;
        while (index > 1) {
            if (heap[index] > heap[index / 2]) {
                int temp = heap[index];
                heap[index] = heap[index / 2];
                heap[index / 2] = temp;
                index /= 2;
            } else break;
        }
    }

    public void insert_Small(int x) {
        heap[++size] = x;
        int index = size;
        while (index > 1) {
            if (heap[index] < heap[index / 2]) {
                int temp = heap[index];
                heap[index] = heap[index / 2];
                heap[index / 2] = temp;
                index /= 2;
            } else break;
        }
    }

    public int delete_Big() {
        int answer = heap[1];
        heap[1] = heap[size--];
        int index = 1;
        while (index * 2 <= size) {
            int left = index * 2, right = left + 1, child;
            if (right <= size) {
                if (heap[left] > heap[right])
                    child = left;
                else
                    child = right;
            } else
                child = left;
            if (heap[child] > heap[index]) {
                int temp = heap[index];
                heap[index] = heap[child];
                heap[child] = temp;
            } else break;
            index = child;
        }
        return answer;
    }

    public int delete_Small() {
        int answer = heap[1];
        heap[1] = heap[size--];
        int index = 1;
        while (index * 2 <= size) {
            int left = index * 2, right = left + 1, child;
            if (right <= size) {
                if (heap[left] < heap[right])
                    child = left;
                else
                    child = right;
            } else
                child = left;
            if (heap[child] < heap[index]) {
                int temp = heap[index];
                heap[index] = heap[child];
                heap[child] = temp;
            } else break;
            index = child;
        }
        return answer;
    }
}
