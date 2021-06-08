function [SSY0_I, SSY0_phi] = init_ssy0(A_I, A_phi, B_I, B_phi, t)


    %% Setup
    % Giles Blaney (Giles.Blaney@tufts.edu) Fall 2019

    rho=[25, 35]; %mm

    % Example data from (Subject 4):
    %   Blaney, G, Sassaroli, A, Pham, T, Fernandez, C, Fantini, S. Phase
    %   dual?slopes in frequency?domain near?infrared spectroscopy for enhanced
    %   sensitivity to brain tissue: First applications to human subjects. J.
    %   Biophotonics. 2019;e201960018. https://doi.org/10.1002/jbio.201960018

    % Physical locations: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    %                     ~   Src1     DetA   DetB     Src2   ~
    %                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    % Data format: Det_Y(time, srcInd)
    % Confirm: ?????src??????????
    %              | srcInd | location | wavelength |
    %              |      1 |     Src1 |          1 690|
    %              |      2 |     Src2 |          1 690|
    %              |      3 |     Src1 |          2 830|
    %              |      4 |     Src2 |          2 830|

    % Parsed format: Y(time, pair, wavelength)
    %                Where "Y" is the datatype (I or phi)

    % Intensity ??????????????????????????????????????phase
    I(:, :, 1)=[A_I(:, 1), B_I(:, 1), B_I(:, 2), A_I(:, 2)]; %counts
    I(:, :, 2)=[A_I(:, 3), B_I(:, 3), B_I(:, 4), A_I(:, 4)]; %counts

    % Phase ??
    phi(:, :, 1)=[A_phi(:, 1), B_phi(:, 1), B_phi(:, 2), A_phi(:, 2)]...
        *pi/180; %rad
    phi(:, :, 2)=[A_phi(:, 3), B_phi(:, 3), B_phi(:, 4), A_phi(:, 4)]...
        *pi/180; %rad


    SSY0_I=[];
    SSY0_phi=[];

    % i1: start point
    % i2: end point
    i1 = 1;
    i2 = length(t);
    inds = i1 : i2;

    SSY0_I = DScalcSSY0(I(inds, :, :), 'intensity', rho);
    SSY0_phi = DScalcSSY0(phi(inds, :, :), 'phase', rho);
end