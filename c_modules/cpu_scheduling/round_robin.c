#include<stdio.h>

int main(){

    int n, tq;

    int bt[20], rem[20], wt[20], tat[20];

    int i, time = 0, remain;

    scanf("%d", &n);

    for(i=0; i<n; i++){
        scanf("%d", &bt[i]);
        rem[i] = bt[i];
    }

    scanf("%d", &tq);

    remain = n;

    while(remain != 0){

        for(i=0; i<n; i++){

            if(rem[i] > 0){

                if(rem[i] <= tq){

                    time += rem[i];

                    rem[i] = 0;

                    tat[i] = time;

                    wt[i] = tat[i] - bt[i];

                    remain--;
                }
                else{

                    rem[i] -= tq;

                    time += tq;
                }
            }
        }
    }

    printf("Process\tBT\tWT\tTAT\n");

    for(i=0; i<n; i++){

        printf("P%d\t%d\t%d\t%d\n",
        i+1, bt[i], wt[i], tat[i]);
    }

    return 0;
}