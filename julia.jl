const max_real = 2.0
const max_imag = max_real
const number = 5000
const max_radius = 50.0
const iters = 100

function iterate_until_escape(z,f)
    z0 = z
    for i = 1:iters
        z0 = f(z0)
        if abs(z0) > max_radius
            return i
        end
    end
    return 0
end

function to_rgb(i)
    if i == 0
        return "255 255 255 "
    else
        b = round(Int,255*(i/iters))
        return "0 $b $b "
    end
end


f(z) = z^2 - 0.5
jul(z) = to_rgb(iterate_until_escape(z,f))

function main()
    open("set.ppm","w") do file
        write(file,"P3\n$number $number\n255\n")
        for y in range(max_imag,stop=-max_imag,length=number)
            for x in range(-max_imag,stop=max_imag,length=number)
                write(file,jul(x+1im*y))
            end
        end
    end
end
main()


