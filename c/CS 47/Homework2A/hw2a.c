#include <stdio.h>
#include <unistd.h>

// I worked with Zane Melcho
unsigned int pflag = 0;			/* positive */
unsigned int nflag = 0;			/* negative */
char *evalue = NULL;		/* mantissa string */
char *svalue = NULL;		/* significand string */

unsigned int get_sign_bit(unsigned int num) {
	if (num <0x80000000 )
	return 0;
	if(num>=0x80000000)
	return 1;
}
unsigned int get_exponent_bits(unsigned int num) {
	unsigned int bitcheck = 2139095040;
	
  return (bitcheck & num) >> 23;			/* you'll change to return something useful */
}

unsigned int get_significand_bits(unsigned int num) {
  unsigned int sigcheck = 0x7FFFFF;
  return sigcheck & num;   /* you'll change to return something useful */
}

unsigned int set_sign_bit(unsigned int sign, unsigned int num) {
   return 0x80000000 | num;	
}

unsigned int set_exponent_bits(unsigned int e, unsigned int num) {
	unsigned int eclear = 0x807FFFFF;
	num = eclear & num;
	return (e <<23) | num; /* you'll change to return something useful */
}

unsigned int set_significand_bits(unsigned int m, unsigned int num) {
	unsigned int mclear = 0xFF800000;
	unsigned int num2;
	num2 = mclear & num;
	return m | num2;			/* you'll change to return something useful */
}


void usage(char *argv[]) {
  printf("Usage:\n");
  printf("%s ARGS <number>\n", argv[0]);
  printf("  where ARGS can be:\n");
  printf("    -p positive sign bit\n");
  printf("    -n negative sign bit\n");
  printf("    -e <int value of exponent>\n");
  printf("    -s <int value of significand>\n");
}


// flag_parse() - Updates the global variables, pflag, nflag, evalue,
// svalue ( see HW2A write-up for details ).
void flag_parse(int argc, char* argv[]) {
  int c;
  opterr = 0;
     
  while ((c = getopt (argc, argv, "pns:e:")) != -1) /* changed to e: not m: */
    switch (c) {
    case 'p':
      pflag = 1;
      break;
    case 'n':
      nflag = 1;
      break;
    case 'e':
      evalue = optarg;
      break;
    case 's':
      svalue = optarg;
      break;
    case '?':
      if (optopt == 'e' || optopt == 's') /* fixed 'e' not 'm' */
	fprintf (stderr, "Option -%c requires an argument.\n", optopt);
      else
	fprintf (stderr,
		 "Unknown option character `%c'.\n",
		 optopt);
      usage(argv);
      return;
    }
  return;
}

int hexchar2int(char c) {
  if ((c >= '0') && (c <= '9')) {
    return c - '0';
  } else {
    switch (c) {
    case 'a':
    case 'b':
    case 'c':
    case 'd':
    case 'e':
    case 'f':
      return 10 + c - 'a';
      break;
    case 'A': 
    case 'B':
    case 'C':
    case 'D':
    case 'E':
    case 'F':
      return 10 + c - 'A';
      break;
    default:
      printf("%c is not a hex character\n", c);
      return -1;
    }
  }  
}
      
// svalue will be a string that if not empty must begin with '0'
// (position 0) and 'x' (position 1), which indicates a hexadecimal
// value
unsigned int signif(char* svalue) {
  int pos;			//character position
  int retval;			// returned value
  char current_char;
  unsigned int digits = 0;	// count hex digits
  for (pos = retval = 0;	// initialize
       svalue[pos] != '\0';	// loop until end of string, svalue
       pos++) {
    current_char = svalue[pos];
    if (pos == 0) {
      if (current_char != '0') {
	printf("hex number literals must start with 0 and you did %c\n",
	       current_char);
	return 0;
      }
    } else if (pos == 1) {
      if ((current_char != 'x') && (current_char != 'X')) {
	printf("hex number literals must start with 0x and you did 0%c\n",
	   current_char);
	return 0;
      }
    } else {
      retval = retval * 16 + hexchar2int(current_char);
      digits++;
    }
  }
  if (digits < 6) {
    for (; digits < 6; digits++) {
      retval = retval * 16;
    }
    retval = retval >> 1;	// shift one bit right
    printf("Warning: significand was padded to yield 0x%x\n", retval);
  }
  return retval;
}

unsigned int signef(char* svalue) {
  int pos;			//character position
  int retval;			// returned value
  char current_char;
  unsigned int digits = 0;	// count hex digits
  for (pos = retval = 0;	// initialize
       svalue[pos] != '\0';	// loop until end of string, svalue
       pos++) {
    current_char = svalue[pos];
    if (pos == 0) {
      if (current_char != '0') {
	printf("hex number literals must start with 0 and you did %c\n",
	       current_char);
	return 0;
      }
    } else if (pos == 1) {
      if ((current_char != 'x') && (current_char != 'X')) {
	printf("hex number literals must start with 0x and you did 0%c\n",
	   current_char);
	return 0;
      }
    } else {
      retval = retval * 16 + hexchar2int(current_char);
      digits++;
    }
  }
  
  return retval;
}
int main(int argc, char* argv[]) {
 int index;
  flag_parse(argc, argv);
   unsigned int num;
  sscanf(argv[argc-1], "%f", &num);
  if (pflag == 1){
  printf("%s \n", argv[argc-1]);
  printf("sign = %d, exponent = 0x%x, significand = 0x%x\n", get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
  }
  if (nflag == 1){
  printf("%s \n", argv[argc-1]);
  printf("sign = %d, exponent = 0x%x, significand = 0x%x\n", get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));	
  num = set_sign_bit(1, num);
  printf("-%s \n", argv[argc-1]);
  printf("sign = %d, exponent = 0x%x, significand = 0x%x\n", get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
	}
  // added call to signif () function to show how to parse significand
  // optional argument
  if (svalue !=NULL && evalue == NULL) {
	unsigned int significand = signif(svalue);
	 printf("%s \n", argv[argc-1]);
	 printf("sign = %d, exponent = 0x%x, significand = 0x%x\n",get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
	num = set_significand_bits(significand, num);
	float* num2 = &num;
	printf("%1f\n", *num2);
	 printf("sign = %d, exponent = 0x%x, significand = 0x%x\n",get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
  }
   if (evalue !=NULL) {
	 printf("%s \n", argv[argc-1]);
	 printf("sign = %d, exponent = 0x%x, significand = 0x%x\n",get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
	 unsigned int exp = signef(evalue);
	 num = set_exponent_bits(exp, num);
	 float* num2 = &num;
	printf("%1f\n", *num2);
	 //printf("%f\n",num);
	 printf("sign = %d, exponent = 0x%x, significand = 0x%x\n",get_sign_bit(num), get_exponent_bits(num), get_significand_bits(num));
  }
  // added some more error checking
  for (index = optind; index < argc - 1; index++)
    printf ("Non-option argument %s\n", argv[index]);

  if (optind != argc - 1) {
    usage(argv);
  }
  //printf("num is %s\n", argv[argc-1]);

  return 0;
}