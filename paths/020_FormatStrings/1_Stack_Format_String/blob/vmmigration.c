/*

gcc vmmigration.c -o vmmigration -m32 -fno-stack-protector

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

int sock;

void socket_send(char *buf) {
    send(sock, buf, strlen(buf), 0);
}

void socket_recv(char *buf, int len) {
    recv(sock, buf, len - 1, 0);
    buf[strlen(buf) - 1] = '\0';
}

void print_menu() {
    socket_send( 
        "Select an option:\n"
        "1. Migrate a VM\n"
        "2. Quit\n");
}

void socket_send_file(char *file) {
    FILE* fd = fopen(file, "r");
    char buf[32];
    size_t nbytes = 0;

    if (fd) {
        while ((nbytes = fread(buf, sizeof(char), 32, fd)) > 0) {
            send(sock, buf, nbytes, 0);
        }
        fclose(fd);
    }
}

void execute_command(char* command) {
    // Not implemented yet :(
}

void migrate_vm() {
    int ip[4], port;
    char vm_name[512];
    char command[1024];

    socket_send("Enter the name of the VM to migrate\n");
    socket_recv(vm_name, sizeof(vm_name));

    socket_send("Enter the destination IP and port (Format: <ip>:<port>)\n");
    socket_recv(command, 32);
    sscanf(command, "%d.%d.%d.%d:%d", &ip[0], &ip[1], &ip[2], &ip[3], &port);

    if ((ip[0] < 0 || ip[0] > 255) ||
        (ip[1] < 0 || ip[1] > 255) ||
        (ip[2] < 0 || ip[2] > 255) ||
        (ip[3] < 0 || ip[3] > 255)) {
        socket_send("Wrong IP format\n");
        return;
    }

    if (port < 0 || port > 65536) {
        socket_send("Wrong port format\n");
        return;
    }

    snprintf(command, sizeof(command) - 1, "MIGRATE %s => %d.%d.%d.%d:%d\n", vm_name, ip[0], ip[1], ip[2], ip[3], port);
    execute_command(command);

    puts(vm_name); // Debug
    printf(command); // Debug
    fflush(stdout);

    socket_send("Successfully migrated VM\n");
}

void get_choice() {
    char *choice_str = (char *) calloc(5, sizeof(char));
    int choice;

    socket_recv(choice_str, 4);
    choice_str[4] = 0;
    choice = atoi(choice_str);
    free(choice_str);

    switch (choice) {
        case 1:
            migrate_vm();
            break;
        case 2:
            socket_send("Good bye!\n");
            exit(0);
            break;
        default:
            print_menu();
            break;
    }
}

void handle(int s) {
    sock = s;

    socket_send_file("welcome_message.txt");

    while (1) {
        print_menu();
        get_choice();
    }
}

// Source: http://www.tutorialspoint.com/unix_sockets/socket_server_example.htm
int main(int argc, char *argv[]) {
    int sockfd, newsockfd, portno, clilen;
    struct sockaddr_in serv_addr, cli_addr;

    int pid, n;

    /* First call to socket() function */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("ERROR opening socket");
        exit(1);
    }
    /* Initialize socket structure */
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(8888);
 
    /* Now bind the host address using bind() call.*/
    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
         perror("ERROR on binding");
         exit(1);
    }
    /* Now start listening for the clients, here 
     * process will go in sleep mode and will wait 
     * for the incoming connection
     */
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    
    while (1) {

        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0) {
            perror("ERROR on accept");
            exit(1);
        }

        /* Create child process */
        pid = fork();
        if (pid < 0) {
            perror("ERROR on fork");
            exit(1);
        }

        if (pid == 0) {
            /* This is the client process */
            close(sockfd);
            handle(newsockfd);
            exit(0);
        } else {
            close(newsockfd);
        }
    } /* end of while */
}
