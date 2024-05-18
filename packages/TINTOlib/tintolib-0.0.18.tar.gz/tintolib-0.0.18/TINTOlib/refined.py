import os
import matplotlib.pyplot as plt
import subprocess
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import euclidean_distances
import math
import pickle
import numpy as np
import pandas as pd
import pickle
from TINTOlib.utils import Toolbox
import platform
import os
from typing import Optional

class REFINED:
    default_problem = "supervised"  # Define the type of dataset [supervised, unsupervised, regression]
    default_verbose = False         # Verbose: if it's true, show the compilation text
    default_hc_iterations = 5       # Number of iterations is basically how many times the hill climbing goes over the entire features and check each feature exchange cost
    default_random_seed = 1         # Default seed for reproducibility
    default_save_image_size = None  # The size in pixels to save the image
    default_n_processors = 8        # Default number of processors

    def __init__(
        self,
        problem: Optional[str] = default_problem,
        verbose: Optional[bool] = default_verbose,
        hcIterations: Optional[int] = default_hc_iterations,
        random_seed: Optional[int] = default_random_seed,
        save_image_size: Optional[int] = default_save_image_size,
        n_processors: Optional[int] = default_n_processors
    ):
        """
        Arguments
        ---------
        problem: (optional) str
            The type of dataset
        verbose: (optional) bool
            If set to True, shows progress messages
        hcIterations: (optional) int
            The number of iterations of hill climbing goes
        random_seed: (optional) int
            The seed for reproduciblitity
        save_image_size: (optional) int
            Defaults to None. The size in pixels for saving the visual results. If save_image_size is None,
            the resulting images will have a size of scale[0]*scale[1] pixels. Otherwise, the size of the image will be
            save_image_size*save_image_size.
        n_processors: (optional) int
            The number of processors to use
        """
        if n_processors <= 1:
            raise ValueError(f"n_processors must be greater than 1 (got {n_processors})")
        
        self.verbose = verbose
        self.problem = problem
        self.hcIterations = hcIterations
        self.random_seed = random_seed
        self.save_image_size = save_image_size
        self.n_processors = n_processors

    def saveHyperparameters(self, filename='objs'):
        """
        This function allows SAVING the transformation options to images in a Pickle object.
        This point is basically to be able to reproduce the experiments or reuse the transformation
        on unlabelled data.
        """
        with open(filename+".pkl", 'wb') as f:
            pickle.dump(self.__dict__, f)
        if self.verbose:
            print("It has been successfully saved in " + filename)


    def loadHyperparameters(self, filename='objs.pkl'):
        """
        This function allows LOADING the transformation options to images in a Pickle object.
        This point is basically to be able to reproduce the experiments or reuse the transformation
        on unlabelled data.
        """
        with open(filename, 'rb') as f:
            variables = pickle.load(f)
        
        for key, val in variables.items():
            setattr(self, key, val)

        if self.verbose:
            print("It has been successfully loaded in " + filename)

    def __saveSupervised(self,classValue,i,folder,matrix_a):
        extension = 'png'  # eps o pdf
        subfolder = str(int(classValue)).zfill(2)  # subfolder for grouping the results of each class
        name_image = str(i).zfill(6)
        route = os.path.join(folder, subfolder)
        route_complete = os.path.join(route, name_image + '.' + extension)
        if not os.path.isdir(route):
            try:
                os.makedirs(route)
            except:
                print("Error: Could not create subfolder")

        shape = int(math.sqrt(matrix_a.shape[0]))
        data = matrix_a.reshape(shape, shape)

        if self.save_image_size is None:
            plt.imsave(route_complete, data, cmap='viridis')
        else:
            fig = plt.figure(figsize=(self.save_image_size, self.save_image_size), dpi=1,)
            ax = fig.add_axes([0, 0, 1, 1], frameon=False)
            ax.imshow(data, cmap='viridis')
            ax.axis('off')
            fig.canvas.draw()
            fig.savefig(fname=route_complete, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
        route_relative = os.path.join(subfolder, name_image+ '.' + extension)
        return route_relative

    def __saveRegressionOrUnsupervised(self, i, folder, matrix_a):
        extension = 'png'  # eps o pdf
        subfolder = "images"
        name_image = str(i).zfill(6)  + '.' + extension
        route = os.path.join(folder, subfolder)
        route_complete = os.path.join(route, name_image)

        if not os.path.isdir(route):
            try:
                os.makedirs(route)
            except:
                print("Error: Could not create subfolder")

        shape = int(math.sqrt(matrix_a.shape[0]))
        data = matrix_a.reshape(shape,shape)

        if self.save_image_size is None:
            plt.imsave(route_complete, data, cmap='viridis')
        else:
            fig = plt.figure(figsize=(self.save_image_size, self.save_image_size), dpi=1,)
            ax = fig.add_axes([0, 0, 1, 1], frameon=False)
            ax.imshow(data, cmap='viridis')
            ax.axis('off')
            fig.canvas.draw()
            fig.savefig(fname=route_complete, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
        route_relative = os.path.join(subfolder, name_image)
        return route_relative

    def __saveImages(self,gene_names,coords,map_in_int, X, Y, nn):

        gene_names_MDS, coords_MDS, map_in_int_MDS=(gene_names,coords,map_in_int)
        X_REFINED_MDS = Toolbox.REFINED_Im_Gen(X, nn, map_in_int_MDS, gene_names_MDS, coords_MDS)
        imagesRoutesArr=[]
        total = Y.shape[0]
        #print(X_REFINED_MDS.shape)
        print("SAVING")
        for i in range(len(X_REFINED_MDS)):
            if self.problem == "supervised":
                route=self.__saveSupervised(Y[i], i, self.folder, X_REFINED_MDS[i])
                imagesRoutesArr.append(route)

            elif self.problem == "unsupervised" or self.problem == "regression" :
                route = self.__saveRegressionOrUnsupervised(i, self.folder, X_REFINED_MDS[i])
                imagesRoutesArr.append(route)
            else:
                print("Wrong problem definition. Please use 'supervised', 'unsupervised' or 'regression'")
            if self.verbose:
                print("Created ", str(i+1), "/", int(total))

        if self.problem == "supervised" :
            data={'images':imagesRoutesArr,'class':Y}
            regressionCSV = pd.DataFrame(data=data)
            regressionCSV.to_csv(self.folder + "/supervised.csv", index=False)
        elif self.problem == "unsupervised":
            data = {'images': imagesRoutesArr}
            regressionCSV = pd.DataFrame(data=data)
            regressionCSV.to_csv(self.folder + "/unsupervised.csv", index=False)
        elif self.problem == "regression":
            data = {'images': imagesRoutesArr,'values':Y}
            regressionCSV = pd.DataFrame(data=data)
            regressionCSV.to_csv(self.folder + "/regression.csv", index=False)


    def __trainingAlg(self, X, Y,Desc):
        """
        This function uses the above functions for the training.
        """
        #Feat_DF = pd.read_csv(data)

        #X = Feat_DF.values;

        #X = X[:100, :-1]


        original_input = pd.DataFrame(data=X)  # The MDS input should be in a dataframe format with rows as samples and columns as features
        feature_names_list = original_input.columns.tolist()  # Extracting feature_names_list (gene_names or descriptor_names)
        if self.verbose:
            print(">>>> Data  is loaded")

        nn = math.ceil(np.sqrt(len(feature_names_list)))  # Image dimension
        Nn = original_input.shape[1]  # Number of features

        transposed_input = original_input.T  # The MDS input data must be transposed , because we want summarize each feature by two values (as compard to regular dimensionality reduction each sample will be described by two values)
        Euc_Dist = euclidean_distances(transposed_input)  # Euclidean distance
        Euc_Dist = np.maximum(Euc_Dist, Euc_Dist.transpose())  # Making the Euclidean distance matrix symmetric

        embedding = MDS(n_components=2, random_state=self.random_seed)  # Reduce the dimensionality by MDS into 2 components
        mds_xy = embedding.fit_transform(transposed_input)  # Apply MDS

        if self.verbose:
            print(">>>> MDS dimensionality reduction is done")

        eq_xy = Toolbox.two_d_eq(mds_xy, Nn)
        Img = Toolbox.Assign_features_to_pixels(eq_xy, nn,verbose=self.verbose)  # Img is the none-overlapping coordinates generated by MDS

        Desc = original_input.columns.tolist()                              # Drug descriptors name
        Dist = pd.DataFrame(data = Euc_Dist, columns = Desc, index = Desc)	# Generating a distance matrix which includes the Euclidean distance between each and every descriptor
        data = (Desc, Dist, Img	)  											# Preparing the hill climbing inputs

        init_pickle_file = "Init_MDS_Euc.pickle"
        with open(init_pickle_file, 'wb') as f:					# The hill climbing input is a pickle, therefore everything is saved as a pickle to be loaded by the hill climbing
            pickle.dump(data, f)

        mapping_pickle_file = "Mapping_REFINED_subprocess.pickle"
        evolution_csv_file = "REFINED_Evolve_subprocess.csv"
        script_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "utils","mpiHill_UF.py"
        )
        
        if 'Windows' == platform.system():
            command = f'mpiexec -np {self.n_processors} python {script_path} --init "{init_pickle_file}" --mapping "{mapping_pickle_file}"  --evolution "{evolution_csv_file}" --num {self.hcIterations}'
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
        else:
            command = f'mpirun -np {self.n_processors} python3 {script_path} --init "{init_pickle_file}" --mapping "{mapping_pickle_file}"  --evolution "{evolution_csv_file}" --num {self.hcIterations}'
            result = subprocess.run(command, shell=True, text=True, capture_output=True)

        if result.returncode != 0:
            raise Exception(result.stderr)

        with open(mapping_pickle_file,'rb') as file:
            gene_names_MDS,coords_MDS,map_in_int_MDS = pickle.load(file)

        self.__saveImages(gene_names_MDS, coords_MDS, map_in_int_MDS, X, Y, nn)

        os.remove(init_pickle_file)
        os.remove(mapping_pickle_file)
        os.remove(evolution_csv_file)

    def generateImages(self,data, folder="/refinedData"):
        """
            This function generate and save the synthetic images in folders.
                - data : data CSV or pandas Dataframe
                - folder : the folder where the images are created
        """
        # Read the CSV
        self.folder = folder
        if type(data) == str:
            dataset = pd.read_csv(data)
            array = dataset.values
            Desc=dataset.columns[:-1].tolist()
        elif isinstance(data, pd.DataFrame):
            array = data.values
            Desc = data.columns[:-1].tolist()

        X = array[:, :-1]
        Y = array[:, -1]

        # Training
        self.__trainingAlg(X, Y,Desc)
        if self.verbose: print("End")