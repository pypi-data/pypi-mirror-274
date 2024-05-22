# ml_algorithm_selector/selector.py

class MLAlgorithmSelector:
    def __init__(self):
        self.questions = {
            "start": self.ask_data_samples,
            "data_samples": self.ask_labelled_data,
            "labelled_data": self.ask_prediction_type,
            "category": self.ask_category_samples,
            "quantity": self.ask_quantity_samples,
            "structure": self.ask_structure_samples,
            "dim_reduction": self.ask_dim_reduction_samples
        }
        self.answers = {}

    def ask_question(self, question):
        response = input(question + " (yes/no): ").strip().lower()
        while response not in ["yes", "no"]:
            response = input("Please answer yes or no: ").strip().lower()
        return response == "yes"

    def ask_data_samples(self):
        more_than_50 = self.ask_question("Do you have more than 50 samples?")
        if more_than_50:
            less_than_100k = self.ask_question("Do you have less than 100k samples?")
            self.answers['data_samples'] = "less_than_100k" if less_than_100k else "more_than_100k"
            return "data_samples"
        else:
            print("Get more data.")
            return None

    def ask_labelled_data(self):
        labelled_data = self.ask_question("Do you have labelled data?")
        self.answers['labelled_data'] = "yes" if labelled_data else "no"
        return "labelled_data"

    def ask_prediction_type(self):
        predicting_category = self.ask_question("Are you predicting a category?")
        if predicting_category:
            self.answers['prediction_type'] = "category"
            return "category"
        predicting_quantity = self.ask_question("Are you predicting a quantity?")
        if predicting_quantity:
            self.answers['prediction_type'] = "quantity"
            return "quantity"
        predicting_structure = self.ask_question("Are you predicting a structure?")
        if predicting_structure:
            self.answers['prediction_type'] = "structure"
            return "structure"
        just_looking = self.ask_question("Are you just looking?")
        if just_looking:
            print("Tough luck.")
            return None
        print("Invalid choice.")
        return None

    def ask_category_samples(self):
        known_categories = self.ask_question("Do you know the number of categories?")
        if known_categories:
            less_than_10k = self.ask_question("Do you have less than 10k samples?")
            if less_than_10k:
                print("Use KMeans.")
            else:
                print("Use MeanShift or VBGMM.")
        else:
            print("Use Spectral Clustering or GMM.")

    def ask_quantity_samples(self):
        less_than_100k = self.answers['data_samples'] == "less_than_100k"
        few_features_important = self.ask_question("Should few features be important?")
        if less_than_100k:
            if few_features_important:
                print("Use Lasso or ElasticNet.")
            else:
                print("Use Ridge Regression or SVR(kernel='linear').")
        else:
            print("Use SVR(kernel='rbf') or Ensemble Regressors.")

    def ask_structure_samples(self):
        less_than_10k = self.ask_question("Do you have less than 10k samples?")
        if less_than_10k:
            print("Use MiniBatch KMeans.")
        else:
            print("Use KMeans.")

    def ask_dim_reduction_samples(self):
        less_than_10k = self.ask_question("Do you have less than 10k samples?")
        if less_than_10k:
            print("Use Randomized PCA.")
        else:
            print("Use Isomap, Spectral Embedding, or LLE.")

    def run(self):
        next_question = "start"
        while next_question:
            next_question = self.questions[next_question]()

def main():
    selector = MLAlgorithmSelector()
    selector.run()
