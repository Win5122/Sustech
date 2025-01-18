#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAT_SIZE 500

/* print array with 1 dimension */
void outputArr_1d(int size, double arr[size])
{
   printf("[");
   for (int i = 0; i < size; i++)
   {
      printf("%f", arr[i]);
      if (i != size - 1)
      {
         printf(", ");
      }
   }
   printf("]");
}

/* print array with 2 dimension */
void outputArr_2d(int size_1, int size_2, double arr[size_1][size_2])
{
   printf("[");
   for (int i = 0; i < size_1; i++)
   {
      printf("[");
      for (int j = 0; j < size_2; j++)
      {
         printf("%f", arr[i][j]);
         if (j != size_2 - 1)
         {
            printf(", ");
         }
      }
      printf("]");
      if (i != size_1 - 1)
      {
         printf(",\n");
      }
   }
   printf("]");
}

/* print 2 array with 2 dimension */
void ouputIntiInfo(int size, double arr_1[size][size], double arr_2[size][size])
{
   printf("Process 0 intialize data:\n");
   outputArr_2d(size, size, arr_1);
   printf(";\n");
   outputArr_2d(size, size, arr_2);
   printf("\n");
   fflush(stdout);
   sleep(1);
}

/* print 1 array with 2 dimension */
void ouputInfo(int world_rank, int size_1, int size_2, double arr[size_1][size_2])
{
   printf("Process %d received data:\n", world_rank);
   outputArr_2d(size_1, size_2, arr);
   printf("\n");
   fflush(stdout);
   sleep(1);
}

/* print 1 array with 1 dimension */
void ouputResuInfo(int world_rank, int size, double arr[size])
{
   printf("Process %d calculate data:\n", world_rank);
   outputArr_1d(size, arr);
   printf("\n");
   fflush(stdout);
   sleep(1);
}

/* brute force matrix multiplication */
void brute_force_matmul(double mat1[MAT_SIZE][MAT_SIZE], double mat2[MAT_SIZE][MAT_SIZE], double res[MAT_SIZE][MAT_SIZE])
{
   /* matrix multiplication of mat1 and mat2, store the result in res */
   for (int i = 0; i < MAT_SIZE; ++i)
   {
      for (int j = 0; j < MAT_SIZE; ++j)
      {
         res[i][j] = 0;
         for (int k = 0; k < MAT_SIZE; ++k)
         {
            res[i][j] += mat1[i][k] * mat2[k][j];
         }
      }
   }
}

/* check whether the obtained result is the same as the intended target */
int checkRes(const double target[MAT_SIZE][MAT_SIZE], const double res[MAT_SIZE][MAT_SIZE])
{
   /* check whether the obtained result is the same as the intended target; if true return 1, else return 0 */
   for (int i = 0; i < MAT_SIZE; ++i)
   {
      for (int j = 0; j < MAT_SIZE; ++j)
      {
         if (res[i][j] != target[i][j])
         {
            return 0;
         }
      }
   }
   return 1;
}

int main(int argc, char *argv[])
{
   /* initialize variables */
   int rank;
   int mpiSize;
   double a[MAT_SIZE][MAT_SIZE],  /* matrix A to be multiplied */
       b[MAT_SIZE][MAT_SIZE],     /* matrix B to be multiplied */
       c[MAT_SIZE][MAT_SIZE],     /* result matrix C */
       bfRes[MAT_SIZE][MAT_SIZE]; /* brute force result bfRes */
   double start, finish;          /* time variables */

   /* initialize MPI */
   MPI_Init(&argc, &argv);
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Comm_size(MPI_COMM_WORLD, &mpiSize);

   /* calculate variables for communication */
   int basicRow = MAT_SIZE / mpiSize;
   int extraRow = MAT_SIZE % mpiSize;
   int recvRows = basicRow + (rank < extraRow ? 1 : 0);
   int sendSize = MAT_SIZE * MAT_SIZE;
   int recvSize = recvRows * MAT_SIZE;

   double *send_a = (double *)malloc(sendSize * sizeof(double));
   double *recv_a = (double *)malloc(recvSize * sizeof(double));

   double *send_c = (double *)malloc(recvSize * sizeof(double));
   double *recv_c = (double *)malloc(sendSize * sizeof(double));

   int sendcounts[mpiSize], displs[mpiSize];

   /* root */
   if (rank == 0)
   {
      /* fill some numbers into the matrix */
      for (int i = 0; i < MAT_SIZE; i++)
      {
         for (int j = 0; j < MAT_SIZE; j++)
         {
            a[i][j] = i + j;
            b[i][j] = i * j;
         }
      }
      // ouputIntiInfo(MAT_SIZE, a, b);

      /* Measure start time */
      start = MPI_Wtime();

      /* calculate the sendcounts and displs */
      int offset = 0;
      for (int i = 0; i < mpiSize; i++)
      {
         sendcounts[i] = (basicRow + (i < extraRow ? 1 : 0)) * MAT_SIZE;
         displs[i] = offset;
         offset += sendcounts[i];
      }

      /* flatten the matrix */
      for (int i = 0; i < MAT_SIZE; i++)
      {
         for (int j = 0; j < MAT_SIZE; j++)
         {
            send_a[i * MAT_SIZE + j] = a[i][j];
         }
      }
   }

   /* send data to each worker */
   MPI_Scatterv(send_a, sendcounts, displs, MPI_DOUBLE, recv_a, recvSize, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   // free(send_a);
   MPI_Bcast(b, MAT_SIZE * MAT_SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

   /* Receive data from root and compute, then send back to root */
   /* a */
   for (int i = 0; i < recvSize / MAT_SIZE; i++)
   {
      for (int j = 0; j < MAT_SIZE; j++)
      {
         a[i][j] = recv_a[i * MAT_SIZE + j];
      }
   }
   // free(recv_a);
   // ouputInfo(rank, recvRows, MAT_SIZE, a);

   /* recieve b */
   // ouputInfo(rank, MAT_SIZE, MAT_SIZE, b);

   /* compute */
   brute_force_matmul(a, b, c);
   // ouputInfo(rank, recvRows, MAT_SIZE, c);

   /* Send back to root */
   for (int i = 0; i < recvRows; i++)
   {
      for (int j = 0; j < MAT_SIZE; j++)
      {
         // flatten the matrix
         send_c[i * MAT_SIZE + j] = c[i][j];
      }
   }
   // ouputResuInfo(rank, recvSize, send_c);
   MPI_Gatherv(send_c, recvSize, MPI_DOUBLE, recv_c, sendcounts, displs, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   // free(send_c);

   if (rank == 0)
   {
      /* Receive results from worker tasks */
      for (int i = 0; i < MAT_SIZE; i++)
      {
         for (int j = 0; j < MAT_SIZE; j++)
         {
            c[i][j] = recv_c[i * MAT_SIZE + j];
         }
      }
      // free(recv_c);
      // ouputInfo(0, MAT_SIZE, MAT_SIZE, c);

      /* Measure finish time */
      finish = MPI_Wtime();
      printf("Done in %f seconds.\n", finish - start);

      /* Compare results with those from brute force */
      brute_force_matmul(a, b, bfRes);
      if (!checkRes(bfRes, c))
      {
         printf("ERROR: Your calculation is not the same as the brute force result, please check!\n");
      }
      else
      {
         printf("Result is correct.\n");
      }
   }

   /* Don't forget to finalize your MPI application */
   MPI_Finalize();
}