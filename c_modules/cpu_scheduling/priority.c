#include<stdio.h>

int main() {

    int n;

    int at[20], bt[20], pr[20];
    int wt[20], tat[20], p[20];

    int i, j, temp;

    scanf("%d", &n);

    // Input

    for(i = 0; i < n; i++) {

        p[i] = i + 1;

        scanf("%d %d %d",
        &at[i],
        &bt[i],
        &pr[i]);
    }

    // Sort by Priority

    for(i = 0; i < n; i++) {

        for(j = i + 1; j < n; j++) {

            if(pr[i] > pr[j]) {

                temp = pr[i];
                pr[i] = pr[j];
                pr[j] = temp;

                temp = bt[i];
                bt[i] = bt[j];
                bt[j] = temp;

                temp = at[i];
                at[i] = at[j];
                at[j] = temp;

                temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    // Waiting Time

    wt[0] = 0;

    for(i = 1; i < n; i++) {

        wt[i] = wt[i - 1] + bt[i - 1];
    }

    // Output

    printf("Process\tAT\tBT\tPR\tWT\tTAT\n");

    for(i = 0; i < n; i++) {

        tat[i] = wt[i] + bt[i];

        printf("P%d\t%d\t%d\t%d\t%d\t%d\n",

        p[i],
        at[i],
        bt[i],
        pr[i],
        wt[i],
        tat[i]);
    }

    return 0;
}
