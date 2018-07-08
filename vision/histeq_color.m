function EI = histeq_color(I)
[row, col, channel] = size(I);
EI = zeros(row, col, channel);
for t = 1:3
    % histogram
    histogram = zeros(1, 256);
    for i = 1:row
        for j = 1:col
            histogram(1, I(i, j, t) + 1) = histogram(1, I(i, j, t) + 1) + 1;
        end
    end

    % cumulative distribution function
    cdf = zeros(1, 256);
    cdf(1, 1) = histogram(1, 1);
    for i = 2:256
        cdf(1, i) = cdf(1, i - 1) + histogram(1, i);
    end

    % point operation
    for i = 1:row
        for j = 1:col
            EI(i, j, t) = cdf(1, I(i, j, t) + 1) * 256 / (row * col);
        end
    end
    
EI = uint8(EI);
end