#include<stdio.h>

int main() {

    int bt[10], wt[10], tat[10];
    int n, i;

    scanf("%d",&n);

    for(i=0;i<n;i++) {
        scanf("%d",&bt[i]);
    }

    wt[0]=0;

    for(i=1;i<n;i++) {
        wt[i]=wt[i-1]+bt[i-1];
    }

    printf("Process\tBT\tWT\tTAT\n");

    for(i=0;i<n;i++) {

        tat[i]=wt[i]+bt[i];

        printf("P%d\t%d\t%d\t%d\n",
        i+1,
        bt[i],
        wt[i],
        tat[i]);
    }

    return 0;
}