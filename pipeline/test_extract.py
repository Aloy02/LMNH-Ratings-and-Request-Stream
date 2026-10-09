from extract import history_file_names


class TestGetHistoryFileNames():
    def test_sorts_list(self):
        file_names = ['lmnh_hist_data_3.csv', 'lmnh_hist_data_2.csv',
                      'lmnh_hist_data_1.csv', 'lmnh_hist_data_0.csv']

        assert history_file_names(file_names) == [
            'lmnh_hist_data_0.csv', 'lmnh_hist_data_1.csv', 'lmnh_hist_data_2.csv', 'lmnh_hist_data_3.csv']

    def test_gets_only_history_files(self):
        file_names = ['lmnh_hist_data_3.csv', 'lmnh_hist_data_2.csv', 'lmnh_hist_data_2.xlsx',
                      'lmnh_hist_data_1.csv', 'lmnh_hist_data_0.csv', 'blah.csv', 'important_hist_data_0.csv']

        assert history_file_names(file_names) == [
            'lmnh_hist_data_0.csv', 'lmnh_hist_data_1.csv', 'lmnh_hist_data_2.csv', 'lmnh_hist_data_3.csv']
