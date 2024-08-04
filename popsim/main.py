from state import StateByBlockGroup

if __name__ == '__main__':
    # for num_sample in [50000, 200000, 1000000, 5000000, 12686469]:
        StateByBlockGroup("17").getSample(100).to_csv('./data/generatedDatasets/IL_dataset_'+ str(100) + '.csv')