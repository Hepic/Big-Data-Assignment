import pandas, algorithms


def main():
    data = pandas.read_csv('datasets/recordings_example.csv', header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    data = data.sort_values(by=['Day', 'Hour'])
    
    algorithms.slow_algorithm(data) 


if __name__ == '__main__':
    main()

