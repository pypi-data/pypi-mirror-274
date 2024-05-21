#include <vector>
#include <string>
#include <map>
#include <array>
#include <queue>
#include <iostream>
using namespace std;
class Region {
public:
    Region();
    int ID;
    std::vector<std::pair<int, int>> pixels;
    std::vector<std::pair<int, int>> boundary;
    int TYPE;
    int value;
    std::string growType;
    std::string shapeType;
    double accessibility;

    // Planimetric attributes
    long pixel_area;
    long area;
    int centroid_X;
    int centroid_Y;
    int perimeter;
    float thickness;
    float length;
    float width;

    // Shape attributes
    float shapeIndex;
    float compactness;
    float elongatedness;
    float asymmetry;
    float orientation;
    float fractal;
    float rectangularity;
    float ellipticity;
    float triangularity;

    // Surface attributes
    float mean_elv_1, mean_slp_1, mean_asp_1, mean_cur_1, mean_curvpro_1, mean_curvpl_1;
    float mean_elv_2, mean_slp_2, mean_asp_2, mean_cur_2, mean_curvpro_2, mean_curvpl_2;

    // Volumetric attributes
    float mean_depth, max_depth, sdv_depth, volume;

    // Thematic attributes

    // Drawing attributes
    // Rectangle
    float tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y;
    // Ellipse
    double a, b;

    double max_distance_centr;
    double mean_distance_centr;
    double mean_dist_bnd;

    // Statistic descriptors
    double min_x, min_y, max_x, max_y;
    double var_x, var_y, covar_xy;
    double lamda1, lamda2;

    // Moment descriptors
    double** m; // moments
    // double u[,];//central moments
    // double n[,];//normalized central moments
    // double phi_1,phi_2,phi_3,phi_4; //invariant moments
    void buildGeometry(const std::vector<std::vector<short>>& binaryImage);
    void print();
    std::string toJsonString() const; 
    void writeToImage(std::vector<std::vector<int>>& image) const;

    
};


class RegionManagement {
    
    std::vector<std::vector<short>> binaryImage;
    std::vector<std::vector<bool>> visited;
    int numRows;
    int numCols;
    int minRow,maxRow,minCol,maxCol;//row and column numbers for exploreBlob to use
    std::map<int, Region> blobs;
    void exploreBlob(int row, int col, Region& blob);
    bool isOnBoundary(int row, int col) const {
        return row == 0 || row == numRows - 1 || col == 0 || col == numCols - 1;
    }
    void enqueueIfValid(std::queue<std::pair<int, int>>& pixelQueue, int row, int col) {
        if (row >= 0 && row < numRows && col >= 0 && col < numCols && !visited[row][col] && binaryImage[row][col] == 1) {
            pixelQueue.push({row, col});
        }
    }
    std::vector<std::pair<int, int>> neighborDefinitions = {
        {-1, 0},  // Up
        {1, 0},   // Down
        {0, -1},  // Left
        {0, 1}    // Right
        // You can add more definitions based on your needs
    };    
public:
    RegionManagement():numRows(0),numCols(0){};
    RegionManagement(const std::vector<std::vector<short>>& binaryImage) : binaryImage(binaryImage) {
        cout<<"Initlaizing the blob algorithm"<<endl;

        try{
            numRows = binaryImage.size();
            numCols = binaryImage[0].size();
            std::cout<<numRows<<","<<numCols<<std::endl;
            visited.resize(numRows, std::vector<bool>(numCols, false));
        }
        catch(std::exception &e){

            cout<<"something is wrong"<<endl;
        }

    
        cout<<"Finished initlaizing the blob algorithm"<<endl;
    };
    void printRegion(int index)
    {
        std::string msg;
        Region region = blobs[index];
        region.print();
        return;
    }
    void printAllRegions()
    {
        for(auto it = blobs.begin(); it != blobs.end();it++){
            it->second.print();
        }
    }
    std::vector<std::vector<int>> writeImage()const;
    //void regionGeneration(int** pOriImg, int nSize, std::vector<RegionClass*>& region_list);
   // int** regionGeneration1(int** pOriImg, int nSize, std::vector<RegionClass*>& region_list);
    //int** regionGeneration2(int** pOriImg, int nSize, std::vector<RegionClass*>& region_list);
   // int** regionGeneration3(int** pOriImg, std::vector<RegionClass*>& region_list);
    //int** regionGeneration4(int** pOriImg, std::vector<RegionClass*>& region_list, int bgValue);
    void regionGeneration();
    void regionGeneration2(int nR, int nC);// the algorithm that splits the image to subregions and generate objects within each region
    //std::vector<std::vector<short>>& create2DArray();
    //std::string& summarizeRegions(); //displaying information of the regions
    void removeSmallObjs(int nSize);
    std::string writeRegionsToJSON() const;
    //int** fillSmallHoles(int** pOriImg, int nSize, std::vector<RegionClass*>& region_list, int bgValue, int fillValue);
};