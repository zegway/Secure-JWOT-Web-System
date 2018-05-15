#include <kore/kore.h>
#include <kore/http.h>
#include <../../libjwt/include/jwt.h>
#include <unistd.h>
#include <time.h>

int		page(struct http_request *);


unsigned char pubkey[450];

size_t key_len;
size_t token_len;

void read_key(unsigned char *key, const char *key_file)
{       
        FILE *fp = fopen(key_file, "r");
        key_len = fread(key, sizeof(key[0]), 450, fp);
        fclose(fp);
        
        key[key_len] = '\0';
}




page(struct http_request *req)
{
	char *authtoken;
	struct kore_buf* buf;
	http_populate_get(req);
	buf = kore_buf_alloc(512);

	if (http_argument_get_string(req, "token", &authtoken)){
		jwt_t *validator=NULL;
		jwt_new(&validator);
		read_key(pubkey, "../public.pem");	
        	int result = jwt_decode(&validator, authtoken, pubkey, key_len);
		if(!result){
			unsigned long exp = jwt_get_grant_int(validator, "exp");
			
			if(exp > (unsigned long) time(NULL))  /*CHECK expiry*/
        			kore_buf_appendf(buf, jwt_get_grant(validator, "user"));
			else
				kore_buf_appendf(buf, "Invalid.");
		}else
			kore_buf_appendf(buf, "Invalid."); 
	}
	else
		kore_buf_appendf(buf, "Invalid");
	
	http_response(req, 200, buf->data, buf->offset);
	kore_buf_free(buf);
	
	return (KORE_RESULT_OK);
}
