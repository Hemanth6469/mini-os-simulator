#include<stdio.h>

int main(){

    int n;

    int bt[20], wt[20], tat[20], p[20];

    int i, j, temp;

    scanf("%d", &n);

    for(i=0; i<n; i++){
        p[i] = i + 1;
        scanf("%d", &bt[i]);
    }

    // Sort by Burst Time
    for(i=0; i<n; i++){
        for(j=i+1; j<n; j++){

            if(bt[i] > bt[j]){

                temp = bt[i];
                bt[i] = bt[j];
                bt[j] = temp;

                temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    wt[0] = 0;

    for(i=1; i<n; i++){
        wt[i] = wt[i-1] + bt[i-1];
    }

    printf("Process\tBT\tWT\tTAT\n");

    for(i=0; i<n; i++){

        tat[i] = wt[i] + bt[i];

        printf("P%d\t%d\t%d\t%d\n",
        p[i], bt[i], wt[i], tat[i]);
    }

    return 0;
}