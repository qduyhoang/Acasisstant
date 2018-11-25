#include <iostream>
#include <fstream>
#include <regex>
#include <map>
#include <vector>
#include <array>
#include <ctime>

using namespace std;

class Account
{
public:
  Account(string num, string name){
    account_number = num;
    acct_holder_name = name;
    balance = 0;
  }

  void addTransaction(string date, string type, string amount)
  {
    string type_str;
    if (type == "D")
      {
	type_str = "deposit";
	balance += stod(amount);
      }
    else if (type == "W")
      {
	type_str = "withdrawal";
	balance -= stod(amount);
      };
    string transaction = date + " " + type_str + " " + "$" + amount;
    transactions.push_back(transaction);
  }

  void showTransaction()
  {
    for (string trans : transactions) {
      cout << "\t" << trans << endl;
    }
  }

  void showInfo()
  {
    string info = "\taccount #:\t" + account_number + "\n\tname:\t" + acct_holder_name + "\n\tbalance:\t$" + to_string(balance) + "\n";
    cout << info;
  }

  float getBalance(){
    return balance;
  }
  string getAccountNumber()
  {
    return account_number;
  }

  string getName()
  {
    return acct_holder_name;
  }

  string print()
  {
    return acct_holder_name + " " + account_number ;
  }

private:
  string account_number;
  string acct_holder_name;
  float balance;
  vector<string> transactions;
};

bool isInteger(const string &s)
{
  if(s.empty() || ((!isdigit(s[0])) && (s[0] != '-') && (s[0] != '+'))) return false;

  char * p;
  strtol(s.c_str(), &p, 10);

  return (*p == 0);
}

string getInput(string prompt)
{
  string user_input;
  cout << prompt;
  cin >> user_input;
  return user_input;
};

string checkInput(string input, string type)
{
  if (type.compare("transaction") == 0)
    if (input.compare("w") == 0 || input.compare("W") == 0)
      {
	return "W";
      }
    else if (input.compare("D") == 0 || input.compare("d") == 0)
      {
	return "D";
      }
    else
      {
	return "";
      };
}

int main(int argc, char **argv)
{
  map<string, Account> acct_map;
  map<string, Account> order;
  ifstream f;
  const char* env_p = getenv("ACCT_LIST");
  if (*env_p)
    {
      f.open(env_p);
    }
  else
    {
      cout << "Please provide an account list" << endl;
    };
  if (f.is_open() && argv[1] != NULL)
    {
      string content;
      bool info;
      bool history;
      bool transaction;
      string cmd_arg = argv[1];
      if (cmd_arg.compare("-i") == 0)
	{
	  info = true;
	  content = "Info\n----\n";
	}
      else if (cmd_arg.compare("-h") == 0)
	{
	  history = true;
	  content = "History\n-----\n";
	}
      else if (cmd_arg.compare("-t") == 0)
	{
	  transaction = true;
	  content = "Transaction\n-----------\n";
	}
      else {
	cout << "Wrong argument" << endl;
	return 1;
      }
      string line;
      while ( getline (f, line) )
      {
	  regex acct_num_reg("(\\d{4}):");
	  regex name_reg("\\d{4}:(\\D+):");
	  regex date_reg(":(\\d{2}\\.\\d{2}\\.\\d{2}):");
	  regex trans_type_reg(":(\\w{1}):");
	  regex amount_reg(":\\w{1}:(\\d+\\.*\\d*)");

	  smatch acct_num_match;
	  smatch name_match;
	  smatch date_match;
	  smatch trans_type_match;
	  smatch amount_match;

	  int rc1 = regex_search(line, acct_num_match, acct_num_reg);
	  int rc2 = regex_search(line, name_match, name_reg);
	  int rc3 = regex_search(line, date_match, date_reg);
	  int rc4 = regex_search(line, trans_type_match, trans_type_reg);
	  int rc5 = regex_search(line, amount_match, amount_reg);

	  if (!(rc1 && rc2 && rc3 && rc4 && rc5))
	    cout << "Wrong input format";

	  string acct_num = acct_num_match[1];
	  string name = name_match[1];
	  string date = date_match[1];
	  string trans_type = trans_type_match[1];
	  string amount = amount_match[1];

	  if (acct_map.count(acct_num) == 0) //If account number doesn't exist
	    {
	      acct_map.insert( pair<string, Account>(acct_num, Account(acct_num, name)));

	    };
	  acct_map.at(acct_num).addTransaction(date, trans_type, amount);
	    }
    

      int i = 1;
      for (map<string, Account>::iterator it=acct_map.begin(); it != acct_map.end(); ++it)
	{
	  order.insert( pair<string, Account>(to_string(i), it->second) );
	  content += to_string(i++) + ") " + it->second.print() + "\n";
	};

      string date, user_input;
      ofstream tmp("tmp.txt");
      while (true)
	{
	  cout << content << "q)uit\n";
	  if (cmd_arg.compare("-t") == 0)
	    {
	      cout << "c)reate a new account" << endl;
	      time_t now = time(0);
	      tm *ltm = localtime(&now);
	      date = to_string(ltm->tm_mon) +  "." + to_string(ltm->tm_mday) + \
	       "." + to_string(ltm->tm_year-100);
	    };
     
	  user_input = getInput("\nEnter choice => ");

	  if (user_input.compare("q") == 0)
	    {
	      break;
	    }
	  else if (user_input.compare("c") == 0)
	    {
	      string name = getInput("\nEnter account holder's name: ");
	      string acct_num = getInput("\nEnter account number: ");
	      string deposit = getInput("Amount of deposit: ");
	      if (!isInteger(acct_num) || !isInteger(deposit))
		{
		  cout << "--------Fail to update!!!--------" <<"\nPlease enter invalid input" << endl;
		  continue;
		}
	      string log = acct_num + ":" + name + ":" + date + ":D:" + deposit;
	      tmp << log << "\n";
	      content+= to_string(i) + ") " + name + " " + acct_num + "\n";
	      i++;
	    }
	  else if (isInteger(user_input))
	    {
	      if ((stoi(user_input) > order.size()) || (user_input.compare("0") == 0))
		{
		  cout << "Number out of range. Please retype." << endl;
		  continue;
		}
	      else if (info)
		{
		  order.at(user_input).showInfo();
		}
	      else if (history)
		{
		  order.at(user_input).showTransaction();
		}
	      else if (transaction)
		{
		  string acct_num = order.at(user_input).getAccountNumber();
		  string name = order.at(user_input).getName();
		  string trans_type = checkInput(getInput("\nWithdrawal or Deposit (w/d)"), "transaction");
		  float cur_balance = order.at(user_input).getBalance();
		  if (trans_type.empty())
		    {
		      cout << "-------please enter valid transaction type (w/d)-------";
		      continue;
		    }
		  string amount = getInput("\nEnter amount:");
		  if (!isInteger(amount))
		    {
		      cout << "--------please enter a valid integer---------";
		      continue;
		    }
		  if ((trans_type.compare("W") == 0) && (stof(amount) > cur_balance))
		    {
		      cout << "------Balance not enough to perform transaction-------" << endl;
		      continue;
		    }
		  string log = acct_num + ":" + name + ":" + date + ":" + trans_type + ":" + amount;
		  tmp << log << endl;
		 };
	    }
	  else
	    {
	      cout << "Please retype your input" << endl;
	      continue;
	    };
	};
      f.close();
      tmp.close();
      ifstream read_from("tmp.txt");
      ofstream write_to(env_p, ios_base::app);
      if (read_from.is_open())
	{
	  while ( getline (read_from, line) )
	    {
	      write_to << line << endl;
	    };
	  read_from.close();
	  write_to.close();
	}
    };
  return 1;
}
