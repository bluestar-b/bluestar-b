#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

int main(int argc, char *argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <times> <address>\n", argv[0]);
    return 1;
  }

  int times = atoi(argv[1]);
  char* address = argv[2];

  CURL *curl;
  CURLcode res;

  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();

  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, address);
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    for (int i = 0; i < times; i++) {
      res = curl_easy_perform(curl);

        if (res != CURLE_OK)
                fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            else
                printf("%d: Request sent successfully\n", i);
        }


    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  return 0;
}
